# coding: utf-8

from json import dumps, loads

import cherrypy
from turbogears import controllers, expose, redirect, view
from turbogears.testutil import make_app, start_server, stop_server
from turbogears.util import simplify_http_accept_header
from webtest import Upload

import pytest


class RandomResource:
    @expose('json')
    def index(self):
        return {'result': 4}  # chosen by fair dice roll; guaranteed random


class ResuorceWithDefault:
    @expose('json')
    def default(self):
        return {'message': 'brought to you by the default view'}


class ResuorceWithIndex:
    @expose('genshi:turbogears.tests.simple')
    def index(self):
        return {'someval': 'SUCCESS!'}


class EmptyResource:
    pass


class JsonResource():
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def cpjson(self):
        return {
            'request_body_json': cherrypy.request.json
        }

    @expose('json')
    @cherrypy.tools.json_in()
    def tgjson(self):
        return {
            'request_body_json': cherrypy.request.json
        }

    @cherrypy.tools.json_in()
    @expose('json')
    def jsontg(self):
        # same as the prior endpoint but with the decorators reversed
        return {
            'request_body_json': cherrypy.request.json
        }


class Root(controllers.RootController):
    jsonthings = JsonResource()
    nodefault = EmptyResource()
    noindex = EmptyResource()
    random = RandomResource()
    withdefault = ResuorceWithDefault()
    withindex = ResuorceWithIndex()

    @expose()
    def plain_expose(self):
        return {}

    @expose()
    def plain_expose_with_params(self, **kw):
        return kw

    @expose('json')
    def some_json(self):
        return {
            'title': 'Foo',
            'abool': False,
            'someval': 'foo',
        }

    @expose('json')
    def custom_json(self, **kw):
        request = controllers.request
        json = request.rfile.input.getvalue()

        return loads(json)

    @expose('genshi:turbogears.tests.simple', allow_json=True)
    def html(self, someval=None, **kw):
        """Basic HTML page, rendered by Genshi.

        Includes the phrase `Paging all ${someval}`.

        """

        return {
            'someval': someval
        }

    @expose('turbogears.tests.simple')
    def html_implied(self, someval=None, **kw):
        return {
            'someval': someval
        }

    @expose('genshi:turbogears.tests.simple', allow_json=False)
    def html_only(self, someval=None, **kw):
        return {
            'someval': someval
        }

    @expose('json')
    def a_b_but_not_c(self, a, b=2):
        return {
            'a': a,
            'b': b,
        }

    @expose('text')
    def plain(self):
        return b'this is the text. exactly.'

    @expose('genshi-text:turbogears.tests.genshi_new_text_format')
    def text_template(self, name='Alice', items=(1,2,3)):
        return {
            'name': name,
            'itemlist': items,
        }

    @expose('json')
    @expose('genshi:turbogears.tests.simple')
    def json_and_html(self):
        return {
            'someval': 'the object format of this thing',
        }

    @expose('genshi:turbogears.tests.simple')
    @expose('json')
    def html_and_json(self):
        # same as the previous endpoint but with the decorators reversed

        return {
            'someval': 'the object format of this thing',
        }

    @expose('json')
    @expose('text')
    @expose('genshi:turbogears.tests.simple')
    def json_and_text_and_html(self):
        accept = simplify_http_accept_header(cherrypy.request.headers.get('Accept', '').lower())

        if accept == 'text/plain':
            return b'the plain format of this thing'
        else:
            return {
                'someval': 'the object format of this thing',
            }

    @expose('genshi:turbogears.tests.simple')
    @expose('json')
    @expose('text')
    def html_and_json_and_text(self):
        # same as the previous endpoint but with the decorators shuffled

        accept = simplify_http_accept_header(cherrypy.request.headers.get('Accept', '').lower())

        if accept == 'text/plain':
            return b'the plain format of this thing'
        else:
            return {
                'someval': 'the object format of this thing',
            }

    @expose()
    def redirect_me(self):
        redirect('/html?someval=misdirection')

    @expose()
    def redirect_me_with_cherrypy(self):
        raise cherrypy.HTTPRedirect('/html?someval=cherrypy misdirection')

    @expose()
    def sneaky_redirect(self):
        raise cherrypy.InternalRedirect('/html?someval=REDACTED ███████████')

    @expose()
    def files_are_fun(self, a_file):
        return {
            'front_9': a_file.fullvalue()[:9]
        }

    @expose()
    def positional_argument(self, arrrrrrg):
        return {}


@pytest.fixture
def app():
    return make_app(Root)


def test_plain_expose_should_return_json(app):
    response = app.get('/plain_expose')

    assert 'application/json' == response.headers['content-type']


def test_plain_expose_should_return_html_format(app):
    params = {
        'tg_template': 'genshi:turbogears.tests.simple',
        'someval': '☭'
    }

    response = app.get('/plain_expose_with_params', params=params)

    assert response.headers['content-type'].startswith('text/html')


def test_html_endpoint_should_return_html(app):
    response = app.get('/html')

    assert response.headers['content-type'].startswith('text/html')


def test_html_endpoint_should_not_return_json(app):
    response = app.get('/html')

    with pytest.raises(AttributeError):  # webtest for “response not JSON”
        response.json


def test_html_endpoint_should_include_rendered_value(app):
    response = app.get('/html?someval=☺')

    assert 'Paging all ☺' in response


def test_html_endpoint_without_engine_should_return_html(app):
    response = app.get('/html_implied')

    assert response.headers['content-type'].startswith('text/html')


def test_index_endpoint_should_be_exposed(app):
    response = app.get('/withindex/')

    assert 'Paging all SUCCESS!' in response


def test_default_endpoint_should_be_exposed(app):
    response = app.get('/withdefault/nonexistent')

    assert 'default view' in response.json['message']


def test_html_endpoint_should_return_json_if_requested(app):
    response = app.get('/html?tg_format=json')

    assert response.json


def test_html_endpoint_should_return_json_if_requested_via_accept_header(app):
    response = app.get('/html', headers={'accept': 'application/json'})

    assert response.json


def test_html_only_endpoint_should_not_return_json_if_requested(app):
    app.get('/html_only?tg_format=json', status=404)


def test_html_only_endpoint_should_not_return_json_if_requested_via_accept(app):
    # I'd prefer:
    #
    #     app.get('/html_only', headers={'Accept': 'application/json'}, status=404)
    #
    # but TG 1.5 instead serves a 200 with a content type not in the request
    # Accept :/

    with pytest.raises(AttributeError):
        response = app.get('/html_only',
                           headers={'Accept': 'application/json'},
                           status='*')
        response.json


def test_json_endpoint_should_return_json(app):
    response = app.get('/some_json')

    assert response.json


def test_json_response_should_include_value(app):
    response = app.get('/some_json')

    assert 'Foo' == response.json['title']


def test_json_endpoint_should_return_json_content_type(app):
    response = app.get('/some_json')

    assert 'application/json' == response.headers['content-type']


# FIXME: support non-dict json
@pytest.mark.parametrize('value', [
    {'a_key': None},
    {'a_key': True},
    {'a_key': 123},
    {'a_key': 'a neato string'},
])
def test_json_value_should_encode_correctly(app, value):
    response = app.post('/custom_json', params=dumps(value))

    assert value == response.json


@pytest.mark.skipif('sys.version_info < (3,0)')
def test_extended_json_value_should_encode_correctly(app):
    response = app.post('/custom_json', params=dumps({'a_key': '♥'}))

    assert '♥' == response.json['a_key']


def test_extra_path_component_should_be_first_positional_argument(app):
    response = app.get('/a_b_but_not_c/smurf')

    assert 'smurf' == response.json['a']


def test_positional_argument_can_be_specified_by_name(app):
    response = app.get('/a_b_but_not_c?a=yay+semantics!')

    assert 'yay semantics!' == response.json['a']


def test_passing_unexpected_argument_should_succeed(app):
    response = app.get('/a_b_but_not_c?a=1&c=BOOM BABY!')


@pytest.mark.skipif('sys.version_info < (3,0)')
def test_text_format_should_be_supported(app):
    response = app.get('/plain')

    assert response.headers['content-type'].startswith('text/plain')


def test_text_format_should_return_exact_text(app):
    response = app.get('/plain')

    assert b'this is the text. exactly.' == response.body


@pytest.mark.xfail('sys.version_info < (3,0)', reason='Genshi misconfig in TG 1.5')
def test_text_template_should_be_supported(app):
    response = app.get('/text_template')

    assert response.headers['content-type'].startswith('text/plain')


def test_subview_index_should_be_exposed(app):
    response = app.get('/random/')

    assert 4 == response.json['result']


def test_subview_without_index_should_not_expose_index(app):
    response = app.get('/noindex/', status=404)


def test_subview_without_default_should_404_for_nonexistent_view(app):
    response = app.get('/nodefault/nonexistent', status=404)


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_html', '/html_and_json'])
def test_two_decorators_should_return_html_as_default(app, path):
    response = app.get(path)

    assert response.headers['content-type'].startswith('text/html')


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_html', '/html_and_json'])
def test_two_decorators_should_return_json_requested_via_accept(app, path):
    response = app.get(path, headers={'Accept': 'application/json'})

    assert response.headers['content-type'].startswith('application/json')


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_html', '/html_and_json'])
def test_two_decorators_should_return_html_requested_via_accept(app, path):
    response = app.get(path, headers={'Accept': 'text/html'})

    assert response.headers['content-type'].startswith('text/html')


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_text_and_html',
                                  '/html_and_json_and_text'])
def test_multiple_decorators_should_return_html_as_default(app, path):
    response = app.get(path)

    assert response.headers['content-type'].startswith('text/html')


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_text_and_html',
                                  '/html_and_json_and_text'])
def test_multiple_decorators_should_return_html_requested_via_accept(app, path):
    response = app.get(path, headers={'Accept': 'text/html'})

    assert response.headers['content-type'].startswith('text/html')


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_text_and_html',
                                  '/html_and_json_and_text'])
def test_multiple_decorators_should_return_json_requested_via_accept(app, path):
    response = app.get(path, headers={'Accept': 'application/json'})

    assert response.headers['content-type'].startswith('application/json')


@pytest.mark.skipif('sys.version_info < (3,0)')
@pytest.mark.parametrize('path', ['/json_and_text_and_html',
                                  '/html_and_json_and_text'])
def test_multiple_decorators_should_return_text_requested_via_accept(app, path):
    response = app.get(path, headers={'Accept': 'text/plain'})

    assert response.headers['content-type'].startswith('text/plain')


def test_turbogears_redirect(app):
    response = app.get('/redirect_me').follow()

    assert 'Paging all misdirection' in response.text


def test_cherrypy_redirect(app):
    response = app.get('/redirect_me_with_cherrypy').follow()

    assert 'Paging all cherrypy misdirection' in response.text


@pytest.mark.skipif('sys.version_info < (3,0)')
def test_cherrypy_internal(app):
    # The redirect should be invisible to the caller → no .follow()
    response = app.get('/sneaky_redirect')

    assert 'Paging all REDACTED ███████████' in response.text


@pytest.mark.skipif('sys.version_info < (3,0)')
def test_expose_file_handling(app):
    response = app.post(
        '/files_are_fun',
        params={'a_file': Upload('./tests/test_expose.py')}
    )

    assert '# coding:' == response.json['front_9']


def test_positional_argument_should_be_accepted(app):
    app.get('/positional_argument/asdf')


def test_omitting_positional_argument_should_404(app):
    app.get('/positional_argument/', status=404)


def test_cp_native_tool_handling(app):
    # sanity check: utilize cherrypy tools — in this case json_in and
    # json_out — but with cp.expose
    response = app.post_json('/jsonthings/cpjson', [0, 1, 2])
    expected = {
        'request_body_json': [0, 1, 2]
    }

    assert expected == response.json


def test_cp_tools_are_run(app):
    # same as the prior test, but utilizing the tg expose dispatch
    # machinery
    response = app.post_json('/jsonthings/tgjson', [0, 1, 2])
    expected = {
        'request_body_json': [0, 1, 2]
    }

    assert expected == response.json


def test_cp_tools_are_run_with_reversed_decorators(app):
    response = app.post_json('/jsonthings/jsontg', [0, 1, 2])
    expected = {
        'request_body_json': [0, 1, 2]
    }

    assert expected == response.json
