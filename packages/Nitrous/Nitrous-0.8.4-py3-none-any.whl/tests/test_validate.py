# coding: utf-8

from turbogears import validate, validators

import pytest


# @validate() requires a self parameter; we'll use this dummy value to
# satisfy the resulting call signatures in the tests below.
self = object()

# we sometimes use a sentinel value to distinguish None from “unspecified”
NoDefault = object()


#
# When decorating a function for validation

def test_should_validate_single_keyword_argument():
    @validate(validators={'foo': validators.StringBool()})
    def boolish(self, foo=False):
        return foo

    assert True == boolish(self, foo='true')


def test_should_accept_validator_default_for_single_missing_keyword_argument():
    @validate(validators={'foo': validators.StringBool(if_empty=True)})
    def boolish(self, foo=None):
        return foo

    assert True == boolish(self)


def test_function_default_should_override_validator_default_for_single_missing_keyword_argument():
    @validate(validators={'foo': validators.StringBool(if_empty=True)})
    def boolish(self, foo=False):
        return foo

    assert False == boolish(self)


def test_should_validate_single_positional_argument():
    @validate(validators={'id': validators.Int()})
    def intish(self, id):
        return id

    assert 1234 == intish(self, '1234')


def test_should_require_a_value_if_validator_specifies_not_empty():
    @validate(validators={'foo': validators.StringBool(not_empty=True)})
    def boolish(self, foo=None, tg_errors=None):
        if tg_errors:
            raise ValueError(repr(tg_errors))
        else:
            return foo

    with pytest.raises(ValueError):
        boolish(self)


def test_should_return_validator_specified_value_on_invalid():
    @validate(validators={'bar': validators.Int(if_invalid=-1)})
    def intish(self, bar=None):
        return bar

    assert -1 == intish(self, bar='☭')


def test_should_accept_positional_argument_for_keyword_parameter():
    @validate(validators={'id': validators.Int()})
    def intish(self, id=None):
        return id

    assert 1234 == intish(self, '1234')


def test_should_distinguish_variable_arguments_from_keyword():
    @validate(validators={'id': validators.Int()})
    def intish(self, id=None, *vpath):
        return id, vpath

    assert 90210, ['1234'] == intish(self, '1234', id='90210')


def test_should_accept_positional_argument_for_keyword_parameter_with_additional():
    @validate(validators={'id': validators.Int()})
    def intish(self, id=None, *vpath):
        return id, vpath

    assert 1234, ['/foo'] == intish(self, '1234', '/foo')


def test_should_return_sentinel_from_function_default():
    @validate(validators={
        'accoms': validators.StringBool(not_empty=True, if_invalid=NoDefault)
    })
    def defaulting(self, accoms=None):
        return accoms

    assert defaulting(self) is NoDefault


def test_should_explode_with_unknown_argument():
    @validate(validators={'enhanced_calm': validators.StringBool()})
    def serenity(self, enhanced_calm=True):
        return enhanced_calm

    with pytest.raises(TypeError):
        serenity(self, exam_type_id='123')


@pytest.mark.xfail('sys.version_info >= (3,0)')
def test_should_raise_typeerror_for_missing_positional_argument():
    # Kinda squirrelly syntax we've created here: in Nitrous’ version of
    # validate, the positional argument is rendered optional by the decorator.
    @validate(validators={'id': validators.Int(if_empty=0)})
    def intish(self, id):
        return id

    with pytest.raises(TypeError):
        intish(self)


def test_should_not_allow_validator_not_present_in_signature():
    @validate(validators={'nargles': validators.national.USPostalCode()})
    def what_are_nargles(self):
        return 'no idea'

    with pytest.raises(TypeError):
        what_are_nargles(self)


def test_should_validate_absent_parameter_for_varkw():
    @validate(validators={
        'nargles': validators.String(if_invalid='no idea', not_empty=True)
    })
    def what_are_nargles(self, **kw):
        return kw['nargles']

    assert 'no idea' == what_are_nargles(self)


def test_multiple_validators_should_validate():
    @validate(validators={
        'a_number': validators.Number(if_invalid=2, not_empty=True),
        'color': validators.OneOf(['green', 'supergreen'],
                                  if_invalid='green', not_empty=True)
    })
    def multipass(self, a_number=None, color=None):
        return {
            'quote': 'act like you have more than a {} word “vocabulary”, {}?'
                     .format(a_number, color)
        }

    quote = multipass(self)['quote']

    assert 'act like you have more than a 2 word “vocabulary”, green?' == quote
