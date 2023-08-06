import cherrypy
from turbogears import controllers, error_handler, expose, validate, validators
from turbogears.testutil import make_app

import pytest


def separate_error_handler(controller, tg_source, tg_errors=None,
                           tg_exceptions=None, *args, **kw):

    return b'separate_error_handler: ' + b'\n'.join(
        str(i).encode('utf-8')
        for i in [controller, tg_source, tg_errors, tg_exceptions, args, kw]
    )


class Root(controllers.RootController):
    @expose()
    def index(self):
        return {}

    @expose()
    @validate(validators={'foo': validators.Constant(value='bar')})
    def why(self, foo):
        return {'foo': foo}

    @expose()
    @validate(validators={'answer': validators.Int(min=42, max=42)})
    def meaning(self, answer):
        return {'meaning': answer}

    @expose()
    @validate(validators={'answer': validators.Int(min=42, max=42)})
    def meaning_with_self_handler(self, answer, tg_errors=None):
        return {'meaning': answer}

    @expose()
    @validate(validators={'answer': validators.Int(min=42, max=42)})
    @error_handler(separate_error_handler)
    def meaning_with_handler(self, answer):
        return {'meaning': answer}

    @expose()
    def i_handle_errors(self, tg_errors=None):
        return (
            b'the errors have been handled ' + str(tg_errors).encode('utf-8')
        )

    @expose()
    @validate(validators={'answer': validators.Int(min=42, max=42)})
    @error_handler(i_handle_errors)
    def meaning_with_exposed_handler(self, answer):
        return {'meaning': answer}

    @expose()
    @validate(validators={'provisional': validators.StringBool()})
    def i_accept_a_stringbool(self, provisional=False):
        return {'provisional': provisional}

    @expose()
    @validate(validators={'id': validators.Number()})
    def i_validate_a_positional_arg(self, id, tg_errors=None):
        if tg_errors:
            raise cherrypy.HTTPError(400, 'Bad input for id: ' + id)

        return {'id': id, 'tg_errors': tg_errors}

    @expose()
    @validate(validators={'enhanced_calm': validators.StringBool()})
    def serenity(self, enhanced_calm=True):
        return {'enhanced_calm': enhanced_calm}


    @validate(validators={'enhanced_calm': validators.StringBool()})
    @expose()
    def ytineres(self, enhanced_calm=True):
        return {'enhanced_calm': enhanced_calm}


@pytest.fixture
def app():
    return make_app(Root)


def test_basic_validator_decorator_should_be_supported(app):
    app.get('/why', params={'foo': 'ignoreme'})


def test_basic_validator_decorator_should_return_validated_value(app):
    response = app.get('/why', params={'foo': 'ignoreme'})

    assert 'bar' == response.json['foo']


def test_validator_accepts_value_in_range(app):
    response = app.get('/meaning', params={'answer': 42})

    assert 42 == response.json['meaning']


def test_validator_accepts_submission_without_argument_having_default(app):
    app.get('/i_accept_a_stringbool', status=200)


def test_validator_substitutes_python_keyword_default_value_without_argument(app):
    response = app.get('/i_accept_a_stringbool', status=200)

    assert response.json['provisional'] is False


def test_validator_correctly_processes_invalid_positional_argument(app):
    app.get('/i_validate_a_positional_arg/foo', status=400)


def test_validator_correctly_processes_valid_positional_argument(app):
    response = app.get('/i_validate_a_positional_arg/12345')

    assert response.json['id'] == 12345  # and _not_ '12345'


def test_validation_error_should_raise_500_with_no_handler(app):
    app.get('/meaning', params={'answer': 1}, status=500)


def test_validation_error_should_not_raise_with_method_as_own_handler(app):
    app.get('/meaning_with_self_handler', params={'answer': 1})


def test_validation_error_should_not_raise_with_declared_handler(app):
    app.get('/meaning_with_handler', params={'answer': 1})


def test_validation_error_should_not_raise_with_declared_exposed_handler(app):
    app.get('/meaning_with_exposed_handler', params={'answer': 1})


def test_unknown_argument_should_be_ignored(app):
    app.get('/serenity', params={'exam_type_id': '123'})


def test_unknown_argument_should_be_ignored_with_decorators_reversed(app):
    app.get('/ytineres', params={'exam_type_id': '123'})


@pytest.mark.xfail
@pytest.mark.parametrize('invalid_value', [None, ''])
def test_validator_rejects_null_value(app, invalid_value):
    app.get('/meaning', params={'answer': invalid_value}, status=500)


@pytest.mark.parametrize('invalid_value', ['blurp', '41'])
def test_validator_rejects_value_out_of_range(app, invalid_value):
    app.get('/meaning', params={'answer': invalid_value}, status=500)
