import inspect

import cherrypy
from turbogears.controllers import Controller
from turbogears.identity import IdentityException, get_identity_errors

import logging
log = logging.getLogger('turbogears.rest')


def __default(self, *vpath, **kw):
    """HTTP verb dispatcher.

    cherrypy default() implementation that chooses the page handler based
    on the HTTP verb used by the request (e.g. GET, POST, PUT, etc.).

    Returns the result of invoking the page handler.

    Raises 404 if the method lookup failed, 400 if the method exists but is
    not exposed or otherwise callable, and 401 if the identity framework
    reports an identity failure.

    """

    http_method = cherrypy.request.method
    method = getattr(self, http_method, None)

    # If there is a vpath, we tried to look up a sub-resource or other exposed
    # method and failed
    if vpath or not method:
        raise cherrypy.HTTPError(404, 'Not found %s' % cherrypy.url(base=''))
    elif not callable(method) or not getattr(method, 'exposed', False):
        raise cherrypy.HTTPError(400, '%s not defined on %s' % (
            http_method, cherrypy.url(base='')))

    try:
        return method(**kw)
    except IdentityException:
        raise cherrypy.HTTPError(401,
                                 'Unauthorized: %s' % get_identity_errors())


def _default(self):
    """Use _cp_config (e.g. cherrypy.tool decorators) from REST endpoints.

    Property getter implementation that copies any _cp_config value defined on
    an exposed REST endpoint to the default() dispatcher method before
    returning it to cherrypy's dispatch framework. This allows REST endpoint
    methods to use cherrypy.tool decorators::

        @expose('json')
        @cherrypy.tools.json_in
        def GET(self):
            # use request.json read by the json_in tool

    Without this wrapper, cherrypy.tool decorators do not work on REST
    endpoints because the cherrypy framework never sees them: it only sees the
    default() method.

    """

    dispatcher = cherrypy.expose()(__default)
    dispatcher.__doc__ = __default.__doc__

    http_verb = cherrypy.request.method
    method = getattr(self, http_verb, None)
    _cp_config = getattr(method, '_cp_config', None)

    if _cp_config:
        dispatcher._cp_config = _cp_config.copy()

    # Convert the dispatch function to a bound method and return it
    return dispatcher.__get__(self)


def RESTContainer(resource_cls_or_name=None):
    """Class decorator for implementing REST-style container controllers.

    For example, to create a list of candidate resources such that::

        /candidates/<id>

    returns a candidate resource for the specified candidate, define the
    candidates controller as

    >>> @RESTContainer('CandidateResource')
    ... class CandidateRootController(Controller):
    ...    pass

    >>> class CandidateResource(RESTResource):
    ...     "Represents a single candidate"

    The resource class must have a constructor that takes a single ID
    as its first parameter and a reference to the parent container as the
    second parameter.

    RESTContainers also do method-based dispatch if the decorated controller
    class does *not* define default::

    >>> @RESTContainer(CandidateResource)
    ... class CandidateRootController(Controller):
    ...    @expose()
    ...    def GET(self):
    ...        # handle request for /candidates

    If the resource class defines a valid_id static function, it is used in
    preference to the str function to determine if an attribute request should
    return an instance of the container's resource class. The valid_id function
    should take a single argument and return it if it is a valid identifier or
    raise ValueError if it is not.

    """

    def decorator(controller_cls):
        def resolve_resource(obj):
            try:
                _cls = obj.resource_cls
            except AttributeError:
                try:
                    module = inspect.getmodule(type(obj))
                    _cls = obj.resource_cls = getattr(module,
                                                      resource_cls_or_name)
                except (TypeError, AttributeError):
                    _cls = obj.resource_cls = resource_cls_or_name

            return _cls

        def _cp_dispatch(self, vpath):
            log.debug('%s vpath: %s', type(self).__name__, vpath)

            try:
                resource_id = vpath[0]
                resource_cls = resolve_resource(self)
                id_validator = getattr(resource_cls, 'valid_id', str)
                return resource_cls(id_validator(resource_id), self)
            except ValueError as e:
                log.debug('Invalid resource id: %s (%s: %s)',
                          resource_id,
                          type(e).__name__,
                          e)
                return vpath

        controller_cls._cp_dispatch = _cp_dispatch

        if not hasattr(controller_cls, 'default'):
            controller_cls.default = property(_default)

        return controller_cls

    return decorator


class RESTResource(Controller):
    """Controller base class that provides HTTP method-based dispatch.

    Subclasses should define methods for each HTTP method they wish to
    implement (e.g. ``GET``).

    See ``README.rst`` and ``controllers.py`` in the example application for
    example usages.

    """

    default = property(_default)
