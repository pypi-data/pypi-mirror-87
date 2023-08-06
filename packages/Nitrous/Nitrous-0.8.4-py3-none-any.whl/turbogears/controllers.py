"""Classes and methods for TurboGears controllers."""

__all__ = ['Controller', 'absolute_url',
    'error_handler', 'exception_handler',
    'expose', 'get_server_name', 'flash', 'redirect',
    'Root', 'RootController', 'url', 'validate']

from functools import wraps
import inspect
import logging
import urllib.request, urllib.parse, urllib.error
import urllib.parse
import types

import attr
import cherrypy
from cherrypy import request, response, url as cp_url
import turbogears.util as tg_util
from turbogears import view, database, errorhandling, config
from turbogears.decorator import wraps_exposed
from turbogears.errorhandling import error_handler, exception_handler
from turbogears.validators import Invalid


log = logging.getLogger('turbogears.controllers')


if config.get('tools.sessions.on', False):
    if config.get('tools.sessions.storage_type') == 'PostgreSQL':
        import psycopg2
        config.update(
            {'tools.sessions.get_db' : psycopg2.connect(
                config.get('sessions.postgres.dsn'))
            })
    # XXX: support for mysql/sqlite/etc here


class BadFormatError(Exception):
    """Output-format exception."""


def validate(form=None, validators=None,
             failsafe_schema=errorhandling.FailsafeSchema.none,
             failsafe_values=None, state_factory=None):
    """Validate input.

    @param form: a form instance that must be passed throught the validation
    process... you must give a the same form instance as the one that will
    be used to post data on the controller you are putting the validate
    decorator on.
    @type form: a form instance

    @param validators: individual validators to use for parameters.
    If you use a schema for validation then the schema instance must
    be the sole argument.
    If you use simple validators, then you must pass a dictionary with
    each value name to validate as a key of the dictionary and the validator
    instance (eg: tg.validators.Int() for integer) as the value.
    @type validators: dictionary or schema instance

    @param failsafe_schema: a schema for handling failsafe values.
    The default is 'none', but you can also use 'values', 'map_errors',
    or 'defaults' to map erroneous inputs to values, corresponding exceptions
    or method defaults.
    @type failsafe_schema: errorhandling.FailsafeSchema

    @param failsafe_values: replacements for erroneous inputs. You can either
    define replacements for every parameter, or a single replacement value
    for all parameters. This is only used when failsafe_schema is 'values'.
    @type failsafe_values: a dictionary or a single value

    @param state_factory: If this is None, the initial state for validation
    is set to None, otherwise this must be a callable that returns the initial
    state to be used for validation.
    @type state_factory: callable or None

    """
    def entangle(func):
        if callable(form) and not hasattr(form, 'validate'):
            init_form = form
        else:
            init_form = lambda self: form

        # Extract defaults from the function signature at definition to
        # supply values for missing arguments during validation
        default_values = tg_util.get_kw_defaults(func)

        @wraps_exposed(func)
        def validate(*args, **kw):
            # do not validate a second time if already validated
            if hasattr(request, 'validation_state'):
                return func(*args, **kw)

            form = init_form(args and args[0] or kw['self'])
            args, kw = tg_util.to_kw(func, args, kw)

            errors = {}
            if state_factory is not None:
                state = state_factory()
            else:
                state = None

            if form:
                value = kw.copy()
                try:
                    kw.update(form.validate(value, state))
                except Invalid as e:
                    errors = e.unpack_errors()
                    request.validation_exception = e
                request.validated_form = form

            if validators:
                if isinstance(validators, dict):
                    for field, validator in validators.items():
                        try:
                            raw_value = \
                                kw.get(field, default_values.get(field, None))
                            kw[field] = validator.to_python(raw_value, state)
                        except Invalid as error:
                            errors[field] = error
                else:
                    try:
                        value = kw.copy()
                        kw.update(validators.to_python(value, state))
                    except Invalid as e:
                        errors = e.unpack_errors()
                        request.validation_exception = e
            request.validation_errors = errors
            request.input_values = kw.copy()
            request.validation_state = state

            if errors:
                kw = errorhandling.dispatch_failsafe(failsafe_schema,
                                            failsafe_values, errors, func, kw)
            args, kw = tg_util.from_kw(func, args, kw)

            return errorhandling.run_with_errors(errors, func, *args, **kw)

        return validate
    return entangle


@attr.s
class ViewConfiguration:
    formats = attr.ib(factory=dict)

    def invoke(self, view_callable, *invoke_args, **kw):
        accept = request.headers.get('Accept', '').lower()
        accept = tg_util.simplify_http_accept_header(accept)

        if accept == 'application/json' or kw.get('tg_format') == 'json':
            format = 'json'
        elif accept == 'text/csv' or kw.get('tg_format') == 'csv':
            format = 'csv'
        elif accept == 'text/plain' or kw.get('tg_format') == 'text':
            format = 'text'
        else:
            format = None

        try:
            args = list(self.formats[format])
        except KeyError:
            raise cherrypy.HTTPError(404)

        args.extend([invoke_args, kw])

        return _execute_func(view_callable, *args)

    def add_format(self, template=None, allow_json=None, format=None, content_type=None,
                   fragment=False, as_format='default', accept_format=None, **options):

        if template is None:
            template = 'json'

        if template == 'text':
            self.formats['text'] = ('text', 'text', content_type or 'text/plain', False, options)
        elif template == 'csv':
            self.formats['csv'] = ('csv', 'text', content_type or 'text/csv', False, options)
        else:
            if allow_json is None:
                allow_json = config.get('tg.allow_json', True)

            if template == 'json' or allow_json:
                self.formats['json'] = ('json', 'json', content_type, False, options)

            if template != 'json':
                self.formats[None] = (template, format, content_type, fragment, options)

        if None not in self.formats:
            self.formats[None] = list(self.formats.values())[0]


def _execute_func(func, template, format, content_type, fragment, options,
                  args, kw):
    """Call controller method and process its output."""

    # get special parameters used by upstream decorators like paginate
    try:
        tg_kw = dict([(k, v) for k, v in list(kw.items()) if k in func._tg_args])
    except AttributeError:
        tg_kw = {}

    # remove excess parameters
    args, kw = tg_util.adapt_call(inspect.unwrap(func), args, kw)

    # add special parameters again
    kw.update(tg_kw)

    env = config.get('environment') or 'development'
    if env == 'development':
        # Only output this in development mode: If it's a field storage object,
        # this means big memory usage, and we don't want that in production
        log.debug("Calling %s with *(%s), **(%s)", func, args, kw)

    output = errorhandling.try_call(func, *args, **kw)

    if template and template.startswith('.'):
        template = func.__module__[:func.__module__.rfind('.')] + template

    return _process_output(output, template, format, content_type,
        fragment=fragment, **options)


def _process_output(output, template, format, content_type, fragment=False,
                    **options):
    """Produce final output form from data returned from a controller method.

    See the expose() arguments for more info since they are the same.

    """

    if str(getattr(response, 'status', '')).startswith('204'):
        # HTTP status 204 indicates a response with no body
        # so there should be no content type header
        try:
            del response.headers['Content-Type']
        except (AttributeError, KeyError):
            pass

        return
    elif isinstance(output, types.GeneratorType):  # let cp handle streaming
        if content_type:
            response.headers['Content-Type'] = content_type
        return output
    elif response.body:
        # If response.body is set, the view handler has already set a response
        # (e.g. a file), so don't process further
        return output

    # FIXME: support CSV

    headers = {'Content-Type': content_type}
    output = view.render(output, template=template, format=format,
                         headers=headers, fragment=fragment, **options)
    content_type = headers['Content-Type']

    if content_type:
        response.headers['Content-Type'] = content_type
    elif template == 'text':
        response.headers['Content-Type'] = 'text/plain'

    return output


def expose(template=None, allow_json=None, format=None, content_type=None,
           fragment=False, as_format='default', accept_format=None, **options):
    """Exposes a method to the web.

    By putting the expose decorator on a method, you tell TurboGears that
    the method should be accessible via URL traversal. Additionally, expose
    handles the output processing (turning a dictionary into finished
    output) and is also responsible for ensuring that the request is
    wrapped in a database transaction.

    You can apply multiple expose decorators to a method, if
    you'd like to support multiple output formats. The decorator that's
    listed first in your code without as_format or accept_format is
    the default that is chosen when no format is specifically asked for.
    Any other expose calls that are missing as_format and accept_format
    will have as_format implicitly set to the whatever comes before
    the ':' in the template name (or the whole template name if there
    is no ':'. For example, <code>expose('json')</code>, if it's not
    the default expose, will have as_format set to 'json'.

    When as_format is set, passing the same value in the tg_format
    parameter in a request will choose the options for that expose
    decorator. Similarly, accept_format will watch for matching
    Accept headers. You can also use both. expose('json', as_format='json',
    accept_format='application/json') will choose JSON output for either
    case: tg_format='json' as a parameter or Accept: application/json as a
    request header.

    Passing allow_json=True to an expose decorator
    is equivalent to adding the decorator just mentioned.

    Each expose decorator has its own set of options, and each one
    can choose a different template or even template engine (you can
    use Kid for HTML output and cheetah for plain text, for example).
    See the other expose parameters below to learn about the options
    you can pass to the template engine.

    Take a look at the
    <a href="tests/test_expose-source.html">test_expose.py</a> suite
    for more examples.

    @param template: 'templateengine:dotted.reference' reference along the
            Python path for the template and the template engine. For
            example, 'kid:foo.bar' will have Kid render the bar template in
            the foo package.
    @keyparam format: format for the template engine to output (if the
            template engine can render different formats. Kid, for example,
            can render 'html', 'xml' or 'xhtml')
    @keyparam content_type: sets the content-type http header
    @keyparam allow_json: allow the function to be exposed as json
    @keyparam fragment: for template engines (like Kid) that generate
            DOCTYPE declarations and the like, this is a signal to
            just generate the immediate template fragment. Use this
            if you're building up a page from multiple templates or
            going to put something onto a page with .innerHTML.
    @keyparam as_format: designates which value of tg_format will choose
            this expose.
    @keyparam accept_format: which value of an Accept: header will
            choose this expose.

    All additional keyword arguments are passed as keyword args to the render
    method of the template engine.

    """

    def expose_view(view_callable):
        view_config = getattr(view_callable, '__config__', None)

        if view_config:
            view_config.add_format(template=template, allow_json=allow_json, format=format, content_type=content_type, fragment=fragment, as_format=as_format, accept_format=accept_format, **options)

            return view_callable
        else:
            view_config = ViewConfiguration()

            view_config.add_format(template=template, allow_json=allow_json, format=format, content_type=content_type, fragment=fragment, as_format=as_format, accept_format=accept_format, **options)

            @wraps(view_callable)
            @cherrypy.expose
            def view(*args, **kw):
                if getattr(request, 'in_transaction', False):
                    return view_config.invoke(view_callable, *args, **kw)
                else:
                    request.in_transaction = True
                    return database.run_with_transaction(view_config.invoke, view_callable, *args, **kw)

            view.__config__ = view_config

            return view
    return expose_view


def flash(message):
    """Set a message to be displayed in the browser on next page display."""
    # message = tg_util.to_utf8(message)
    if len(message) > 4000:
        log.warning('Flash message exceeding maximum cookie size!')
    response.cookie['tg_flash'] = message
    response.cookie['tg_flash']['path'] = '/'


def _get_flash():
    '''Retrieve the flash message (if one is set), clearing the message.'''
    request_cookie = request.cookie
    response_cookie = response.cookie

    def clearcookie():
        response_cookie['tg_flash'] = ''
        response_cookie['tg_flash']['expires'] = 0
        response_cookie['tg_flash']['path'] = '/'

    if 'tg_flash' in response_cookie:
        message = response_cookie['tg_flash'].value
        response_cookie.pop('tg_flash')
        if 'tg_flash' in request_cookie:
            # New flash overrided old one sitting in cookie. Clear that old cookie.
            clearcookie()
    elif 'tg_flash' in request_cookie:
        message = request_cookie.value_decode(request_cookie['tg_flash'].value)[0]
        if 'tg_flash' not in response_cookie:
            clearcookie()
    else:
        message = None

    # if message:
    #     message = str(message, 'utf-8')

    return message


class Controller(object):
    """Base class for a web application's controller.

    It is important that your controllers inherit from this class, otherwise
    ``identity.SecureResource`` and ``identity.SecureObject`` will not work
    correctly.

    """

    is_app_root = None


class RootController(Controller):
    """Base class for the root of a web application.

    Your web application must have one of these. The root of your application
    is used to compute URLs used by your app.

    """

    is_app_root = True

Root = RootController


class ExposedDescriptor(object):
    """Descriptor used by RESTMethod to tell if it is exposed."""

    def __get__(self, obj, cls=None):
        """Return True if object has a method for HTTP method of current request
        """
        if cls is None:
            cls = obj
        cp_methodname = cherrypy.request.method
        methodname = cp_methodname.lower()
        method = getattr(cls, methodname, None)
        if callable(method) and getattr(method, 'exposed', False):
            return True
        raise cherrypy.HTTPError(405, '%s not allowed on %s' % (
            cp_methodname, cherrypy.request.browser_url))


class RESTMethod(Controller):
    """Allow REST style dispatch based on different HTTP methods.

    For an elaborate usage example see turbogears.tests.test_restmethod.

    In short, instead of an exposed method, you define a sub-class of
    RESTMethod inside the controller class and inside this class you define
    exposed methods named after each HTTP method that should be supported.

    Example::

        class Controller(controllers.Controller):

            class article(copntrollers.RESTMethod):
                @expose()
                def get(self, id):
                    ...

                @expose()
                def post(self, id):
                    ...

    """
    exposed = ExposedDescriptor()

    def __init__(self, *l, **kw):
        methodname = cherrypy.request.method.lower()
        self.result = getattr(self, methodname)(*l, **kw)

    def __iter__(self):
        return iter(self.result)


def url(tgpath, tgparams=None, **kw):
    """Computes relocatable URLs.

    tgpath can be a list or a string. If the path is absolute (starts with a
    "/"), the server.webpath, SCRIPT_NAME and the approot of the application
    are prepended to the path. In order for the approot to be detected
    properly, the root object must extend controllers.RootController.

    Query parameters for the URL can be passed in as a dictionary in
    the second argument and/or as keyword parameters where keyword args
    overwrite entries in the dictionary.

    Values which are lists or tuples will create multiple key-value pairs.

    tgpath may also already contain a (properly escaped) query string seperated
    by a question mark, in which case additional query params are appended.

    """
    if not isinstance(tgpath, str):
        tgpath = '/'.join(list(tgpath))
    if tgpath.startswith('/'):
        webpath = config.server.get('server.webpath', '')
        if tg_util.request_available():
            tgpath = cp_url(tgpath, relative='server')
            if not request.script_name.startswith(webpath):
                # the virtual path dispatcher is not running
                tgpath = webpath + tgpath
        elif webpath:
            # the server is not running
            tgpath = webpath + tgpath
    if tgparams is None:
        tgparams = kw
    else:
        try:
            tgparams = tgparams.copy()
            tgparams.update(kw)
        except AttributeError:
            raise TypeError('url() expects a dictionary for query parameters')
    args = []
    for key, value in tgparams.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            pairs = [(key, v) for v in value]
        else:
            pairs = [(key, value)]
        for k, v in pairs:
            if v is None:
                continue
            if isinstance(v, str):
                v = v.encode('utf-8')
            args.append((k, v))
    if args:
        query_string = urllib.parse.urlencode(args, True)
        if '?' in tgpath:
            tgpath += '&' + query_string
        else:
            tgpath += '?' + query_string
    return tgpath


def get_server_name():
    """Return name of the server this application runs on.

    Respects 'Host' and 'X-Forwarded-Host' header.

    See the docstring of the 'absolute_url' function for more information.

    """
    get = config.get
    h = request.headers
    host = get('tg.url_domain') or h.get('X-Forwarded-Host', h.get('Host'))
    if not host:
        host = '%s:%s' % (get('server.socket_host', 'localhost'),
            get('server.socket_port', 8080))
    return host


def absolute_url(tgpath='/', params=None, **kw):
    """Return absolute URL (including schema and host to this server).

    Tries to account for 'Host' header and reverse proxying
    ('X-Forwarded-Host').

    The host name is determined this way:

    * If the config setting 'tg.url_domain' is set and non-null, use this value.
    * Else, if the 'base_url_filter.use_x_forwarded_host' config setting is
      True, use the value from the 'Host' or 'X-Forwarded-Host' request header.
    * Else, if config setting 'base_url_filter.on' is True and
      'base_url_filter.base_url' is non-null, use its value for the host AND
      scheme part of the URL.
    * As a last fallback, use the value of 'server.socket_host' and
      'server.socket_port' config settings (defaults to 'localhost:8080').

    The URL scheme ('http' or 'http') used is determined in the following way:

    * If 'base_url_filter.base_url' is used, use the scheme from this URL.
    * If there is a 'X-Use-SSL' request header, use 'https'.
    * Else, if the config setting 'tg.url_scheme' is set, use its value.
    * Else, use the value of 'cherrypy.request.scheme'.

    """
    get = config.get
    use_xfh = get('base_url_filter.use_x_forwarded_host', False)
    if request.headers.get('X-Use-SSL'):
        scheme = 'https'
    else:
        scheme = get('tg.url_scheme')
    if not scheme:
        scheme = request.scheme
    base_url = '%s://%s' % (scheme, get_server_name())
    if get('base_url_filter.on', False) and not use_xfh:
        base_url = get('base_url_filter.base_url').rstrip('/')
    return '%s%s' % (base_url, url(tgpath, params, **kw))


def redirect(redirect_path, redirect_params=None, **kw):
    """Redirect (via cherrypy.HTTPRedirect).

    Raises the exception instead of returning it, this to allow
    users to both call it as a function or to raise it as an exception.

    """
    if not isinstance(redirect_path, str):
        redirect_path = '/'.join(list(redirect_path))
    if not (redirect_path.startswith('/')
            or redirect_path.startswith('http://')
            or redirect_path.startswith('https://')):
        redirect_path = urllib.parse.urljoin(request.path_info, redirect_path)
    raise cherrypy.HTTPRedirect(url(redirect_path, redirect_params, **kw))
