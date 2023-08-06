# coding: utf-8

from json import dumps, loads

import cherrypy
from turbogears import config, controllers, expose, identity, validate, validators, view, visit
from turbogears.database import session
from turbogears.identity.saprovider import TG_Group, TG_Permission, TG_User
from turbogears.testutil import make_app, start_server, stop_server
from turbogears.util import simplify_http_accept_header

import pytest


_test_accounts = {
    'admin': 'admin',
    'alice': 'secret',
}

_test_groups = [
    # group name, ['permissions'], ['users']
    ('admin', ['like_a_boss'], ['admin'])
]


def as_(user_name):
    try:
        return {
            'user_name': user_name,
            'password': _test_accounts[user_name],
            'login': 'Login',
        }
    except KeyError:
        pass


def _make_users():
    "Create test users using default saprovider models."

    for account in _test_accounts.items():
        user = TG_User()
        session.add(user)
        user.user_name, user.password = account

    session.flush()

    for group_name, permissions, users in _test_groups:
        group = TG_Group()
        session.add(group)
        group.group_name = group_name

        for user in users:
            group.users.append(
                session.query(TG_User).filter_by(user_name=user).one()
            )

        for permission_name in permissions:
            permission = TG_Permission()
            session.add(permission)
            permission.permission_name = permission_name

            group.permissions.append(permission)

    session.flush()


@pytest.fixture(scope='session', autouse=True)
def _start_server():
    # visits are a prerequisite for identity
    config.update({
        'visit.on': True,
        'visit.manager': 'sqlalchemy',
        'identity.on': True,
        'identity.provider': 'sqlalchemy',
        'identity.failure_url': '/identity_failed',
        'tools.encode.on': False,
    })

    start_server()

    _make_users()


@pytest.fixture()
def app():
    return make_app(Root)


class AdminArea(controllers.Controller, identity.SecureResource):
    require = identity.in_group('admin')

    @expose()
    def lounge(self):
        return {}


class Root(controllers.RootController):
    admin = AdminArea()

    @identity.require(identity.not_anonymous())
    @expose('genshi:turbogears.tests.simple')
    def index(self, **kw):
        return {
            'someval': identity.current.user.user_name
        }

    @expose('text')
    @identity.require(identity.not_anonymous())
    @cherrypy.tools.encode(encoding='utf-8', add_charset=True)
    def some_utf8_text(self):
        # Test compatibility of the identity decorator and cherrypy tools.
        # This handler is protected by an identity requirement and uses a
        # cherrypy tool to adapt the returned Unicode string to utf-8.
        #
        # If the tool doesn't fire, the result of this endpoint is
        #
        #    ValueError: Page handlers MUST return bytes. Use tools.encode if you wish to return unicode.

        return 'Éowyn'

    @expose()
    def imperative_group_check(self):
        if 'admin' not in identity.current.groups:
            raise identity.IdentityException('Bounced!')

        return {}

    @expose()
    def cp_error(self, code=403):
        raise cherrypy.HTTPError(code or 403)

    @identity.require(identity.not_anonymous())
    @expose('json')
    def json_for_users(self, should_asplode=False, **kw):
        if should_asplode:
            raise ValueError('BOOM!!1')

        return {}

    @identity.require(identity.in_group('admin'))
    @expose('json')
    def json_for_admins(self, **kw):
        return {}

    @identity.require(identity.has_permission('like_a_boss'))
    @expose('json')
    def json_like_a_boss(self, **kw):
        return {}

    @expose()
    @identity.require(identity.not_anonymous())
    @validate(validators={'foo': validators.String(if_empty='42')})
    def validate_me(self, foo=None, *args, **kw):
        return {'foo': foo}

    @expose()
    @identity.require(identity.not_anonymous())
    def drop_extraneous(self, foo=None):
        return {'foo': foo}

    @expose()
    @validate(validators={'foo': validators.String(if_empty='42')})
    @identity.require(identity.not_anonymous())
    def drop_and_validate(self, foo=None):
        return {'foo': foo}

    @expose()
    @cherrypy.tools.encode(encoding='utf-8', add_charset=True)
    def identity_failed(self, **kw):
        """This is the Identity Failure URL.

        Set in the configuration specified in the app fixture above.

        """

        validated = bool(getattr(cherrypy.request, 'validation_state', None))

        return 'Fail-yore! (validation run: {})'.format(validated)


def test_when_requested_anonymously_private_resource_should_raise(app):
    app.get('/', status=403)


def test_identity_failure_should_trigger_configured_failure_endpoint(app):
    response = app.get('/', status=403)

    assert 'Fail-yore!' in response.text


def test_when_requested_anonymously_user_json_resource_should_raise(app):
    app.get('/json_for_users', status=403)


@pytest.mark.xfail(reason='COREBT-13179')
def test_when_requested_anonymously_imperative_resource_should_raise(app):
    app.get('/imperative_group_check', status=403)


def test_when_requested_with_login_private_resource_should_succeed(app):
    # authenticate & make request in one shot using default TG identity
    # machinery; pattern from original TG test suite
    response = app.get('/', params=as_('alice'))

    assert 'Paging all alice' in response.text


def test_when_requested_as_user_private_json_resource_should_succeed(app):
    response = app.get('/json_for_users', params=as_('alice'))

    assert 'application/json' == response.headers['content-type']


def test_when_requested_as_user_exception_should_not_trigger_identity_failure(app):
    params = as_('alice')
    params['should_asplode'] = 'definitely'

    response = app.get('/json_for_users', params=params, status=500)

    assert 'Fail-yore!' not in response.text


@pytest.mark.parametrize('code', [400, 401, 403, 404, 500, 501, 503])
def test_imperative_HTTPError_should_not_trigger_identity_failure(app, code):
    response = app.get('/cp_error', params={'code': code}, status=code)

    assert 'Fail-yore!' not in response.text


def test_when_requested_without_group_json_resource_should_raise(app):
    app.get('/json_for_admins', params=as_('alice'), status=403)


def test_when_requested_with_group_json_resource_should_succeed(app):
    app.get('/json_for_admins', params=as_('admin'))


def test_when_requested_without_permission_json_resource_should_raise(app):
    app.get('/json_like_a_boss', params=as_('alice'), status=403)


def test_when_requested_with_permission_json_resource_should_succeed(app):
    app.get('/json_like_a_boss', params=as_('admin'))


def test_when_requested_anonymously_sub_resource_should_raise(app):
    app.get('/admin/lounge', status=403)


def test_identity_failure_should_preempt_validation(app):
    response = app.get('/validate_me', status=403)

    assert 'validation run: False' in response


def test_identity_success_should_allow_validation(app):
    response = app.get('/validate_me', params=as_('alice'))

    assert {'foo': '42'} == response.json


def test_with_identity_should_drop_extraneous_args(app):
    params = as_('alice')
    params.update({'foo': 'here!', 'extraneous': 'gone!'})

    response = app.get('/drop_extraneous', params=params)

    assert {'foo': 'here!'} == response.json


def test_with_identity_should_drop_extraneous_args_and_validate_rest(app):
    params = as_('alice')
    params.update({'extraneous': 'gone!'})

    response = app.get('/drop_and_validate', params=params)

    assert {'foo': '42'} == response.json


@pytest.mark.skipif('sys.version_info < (3,0)')
def test_tool_sanity(app):
    @cherrypy.expose
    @cherrypy.tools.encode(encoding='utf-8')
    def some_unicode():
        return '☭'

    cherrypy.tree.mount(some_unicode, '/utf_me')

    response = app.get('/utf_me')

    assert '☭'.encode('utf-8') == response.body


def test_identity_and_tool_should_restrict_access(app):
    app.get('/some_utf8_text', status=403)


@pytest.mark.skipif('sys.version_info < (3,0)')
def test_identity_and_tool_should_cooperate(app):
    response = app.get('/some_utf8_text', params=as_('alice'))

    assert 'Éowyn'.encode('utf-8') == response.body
