import json
import typing
from unittest import mock
import uuid

import pytest

from horkos import checks


def test_json_string_checker_happy_path():
    """Should be able check a valid json string."""
    value = json.dumps({'foo': 'bar'})
    checker = checks.JsonString()

    passes = checker(value)

    assert passes


def test_json_string_checker_bad_json():
    """Should be able check an invalid json string."""
    checker = checks.JsonString()

    passes = checker('<xml></xml>')

    assert not passes


def test_json_array_string_checker_happy_path():
    """Should be able check a valid json array string."""
    value = json.dumps(['foo', 'bar'])
    checker = checks.JsonArrayString()

    passes = checker(value)

    assert passes


def test_json_object_string_checker_happy_path():
    """Should be able check a valid json object string."""
    value = json.dumps({'foo': 'bar'})
    checker = checks.JsonObjectString()

    passes = checker(value)

    assert passes


def test_json_string_checker_wrong_type():
    """Should be able check a value of the wrong type."""
    checker = checks.JsonString()

    passes = checker(12)

    assert not passes


def test_choice_checker_happy_path():
    """
    Should be able to check that a value is within a valid set of
    choices.
    """
    checker = checks.Choice(options=['foo', 'bar'])

    passes = checker('foo')

    assert passes


def test_choice_checker_bad_value():
    """
    Should be able to see that a value is not within a valid set of
    choices.
    """
    checker = checks.Choice(options=['foo', 'bar'])

    passes = checker('fizbuzz')

    assert not passes


def test_email_checker_happy_path():
    """Should be able to validate an email."""
    checker = checks.Email()

    passes = checker('could.be@an-email.com')

    assert passes


def test_email_checker_bad_value():
    """Should be able to identify an invalid email."""
    checker = checks.Email()

    passes = checker('for-sure-not-valid')

    assert not passes


def test_uuid_checker_happy_path():
    """Should be able to validate a uuid."""
    value = str(uuid.uuid4())
    checker = checks.Uuid()

    passes = checker(value)

    assert passes


def test_uuid_checker_bad_value():
    """Should be able to identify a non-uuid."""
    value = '398l159z-8m4n-455o-pqr0-75s66tu074jk'
    checker = checks.Uuid()

    passes = checker(value)

    assert not passes


def test_iso_timestamp_checker_happy_path():
    """Should be able to identify a iso compliant timestamp."""
    value = '2020-03-18T12:34:56'
    checker = checks.IsoTimestamp()

    passes = checker(value)

    assert passes


def test_max_checker_happy_path():
    """Should be able to identify a value less than the limit."""
    value = 0.5
    checker = checks.Maximum(limit=1)

    passes = checker(value)

    assert passes


def test_min_checker_happy_path():
    """Should be able to identify a value greater than the limit."""
    value = 1
    checker = checks.Minimum(limit=1)

    passes = checker(value)

    assert passes


@mock.patch('json.loads')
def test_keyboard_interupts_surface(loads: mock.MagicMock):
    """A keyboard interupt should always get reraised."""
    loads.side_effect = KeyboardInterrupt
    checker = checks.JsonString()

    with pytest.raises(KeyboardInterrupt):
        checker('some-value')


JSON_CHECKERS = [
    (checks.JsonString, json.dumps({'f': float('NaN')})),
    (checks.JsonObjectString, json.dumps({'f': float('NaN')})),
    (checks.JsonArrayString, json.dumps([float('NaN')])),
]


@pytest.mark.parametrize('checker_cls,value', JSON_CHECKERS)
def test_json_checker_doesnt_tolerate_nan(
        checker_cls: typing.Callable,
        value: str,
):
    """Should fail to validate json with Nans."""
    value = json.dumps({'foo': float('NaN')})
    checker = checker_cls()

    passes = checker(value)

    assert not passes


def test_max_length_checker_happy_path():
    """Should be able to validate a string within the max length."""
    value = 'short'
    checker = checks.MaxLength(limit=10)

    passes = checker(value)

    assert passes


def test_max_length_checker_sad_path():
    """Should be able to reject a string outside the max length."""
    value = 'very-very-very-very-long'
    checker = checks.MaxLength(limit=10)

    passes = checker(value)

    assert not passes
