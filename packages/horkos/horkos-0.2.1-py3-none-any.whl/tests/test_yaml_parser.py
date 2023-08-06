import os.path
import typing

import pytest

from horkos import _yaml_parser
from horkos import errors


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(DIR_PATH, 'resources')


def test_load_schema():
    """Should be able to create a schema from a yaml file without error."""
    yaml_path = os.path.join(RESOURCE_PATH, 'sample.yaml')

    _yaml_parser.load_schema(yaml_path)


def test_schema_process():
    """Should be able to process a record with the schema."""
    raw_schema = {
        'name': 'foobar',
        'description': 'The details',
        'fields': {
            'first_field': {
                'type': 'string',
                'description': 'This is a description',
                'checks': [
                    {'name': 'regex', 'args': {'regex': r'\d+'}}
                ]
            },
            'second_field': {
                'type': 'string',
                'description': 'Some description',
                'required': False,
                'nullable': True,
                'checks': [
                    'json'
                ]
            }
        }
    }
    schema = _yaml_parser.load_schema(raw_schema)

    result = schema.process({'first_field': 123456})

    assert result['first_field'] == '123456'
    assert result['second_field'] == None


def test_find_errors_non_nullable_fields():
    """Should be able to identify null values in non-nullable fields."""
    raw_schema = {
        'name': 'name',
        'fields': {
            'fieldId': {'type': 'string', 'nullable': False}
        }
    }
    schema = _yaml_parser.load_schema(raw_schema)

    with pytest.raises(errors.RecordValidationError) as err:
        schema.process({'fieldId': None})

    assert 'Non-nullable fields are null: fieldId' in str(err.value)


def test_load_schema_with_custom_checker():
    """A custom checker should be handled without error."""
    raw_schema = {
        'name': 'name',
        'fields': {
            'fieldId': {'type': 'string', 'checks': ['custom']}
        }
    }
    custom = {'custom': lambda x: True}

    _yaml_parser.load_schema(
        raw_schema, custom_checkers=custom
    )


def test_find_errors_required_fields():
    """Should be able to identify required fields."""
    raw_schema = {
        'name': 'name',
        'fields': {
            'fieldId': {'type': 'string', 'required': True}
        }
    }
    schema = _yaml_parser.load_schema(raw_schema)

    with pytest.raises(errors.RecordValidationError) as err:
        schema.process({})


    assert 'Required fields are missing: fieldId' in str(err.value)


def test_schema_with_unknown_checker():
    """A SchemaValidationError should be raised if we don't know the checker"""
    raw_schema = {
        'name': 'name',
        'fields': {
            'fieldId': {'type': 'str', 'checks': ['unknown']}
        }
    }

    with pytest.raises(errors.SchemaValidationError) as err:
        _yaml_parser.load_schema(raw_schema)

    msg = 'In "fields.fieldId.checks[0]" check name "unknown" is unknown.'
    assert msg in str(err.value)


SCENARIOS = [
    {'name': 'custom', 'args': {'foo': 'bar', 'fizz': 'buzz'}},
    {'name': 'custom', 'args': {}},
    {'name': 'regex', 'args': {'any': 'thing'}},
]


@pytest.mark.parametrize('check', SCENARIOS)
def test_schema_with_bad_checker(check: dict):
    """If given a bad checker a validation error should be raised."""

    def custom(value, foo, boo='faz'):
        """Custom check function"""

    raw_schema = {
        'name': 'name',
        'fields': {
            'fieldId': {'type': 'str', 'checks': [check]}
        }
    }

    with pytest.raises(errors.SchemaValidationError) as err:
        _yaml_parser.load_schema(
            raw_schema, custom_checkers={'custom': custom}
        )

    assert 'Invalid arguments in "fields.fieldId.checks[0]"' in str(err.value)


SCENARIOS = [
    ({}, '"name" is required'),
    ({'name': {}}, '"name" must be of type str'),
]


@pytest.mark.parametrize('schema, msg', SCENARIOS)
def test_standardize_schema_errors(schema: typing.Any, msg: str):
    """If given a bad schema an error should be raised."""
    with pytest.raises(errors.SchemaValidationError) as err:
        _yaml_parser._standardize_schema(schema)

    assert msg in str(err.value)


def test_standardize_field_errors():
    """If given a bad field an error should be raised."""
    field = {'type': 'bool', 'description': 'foo', 'labels': []}

    with pytest.raises(errors.SchemaValidationError) as err:
        _yaml_parser._standardize_field(field, 'field_id')

    msg = '"fields.field_id.labels" must be of type dict'
    assert msg in str(err.value)


SCENARIOS = [
    ({}, '"prefix.name" is required'),
    ({'name': []}, '"prefix.name" must be a string'),
    ({'name': 'something', 'args': []}, '"prefix.args" must be a dictionary'),
    ([], '"prefix" must be a string or dictionary'),
]


@pytest.mark.parametrize('check, msg', SCENARIOS)
def test_standardize_check_errors(check: typing.Any, msg: str):
    """If given a bad check an error should be raised."""
    with pytest.raises(errors.SchemaValidationError) as err:
        _yaml_parser._standardize_check(check, 'prefix')

    assert msg in str(err.value)


def test_schema_process_with_errors():
    """Should get all check errors at once."""
    raw_schema = {
        'name': 'foobar',
        'description': 'The details',
        'fields': {
            'first_field': {
                'type': 'string',
                'description': 'This is a description',
                'checks': [
                    {'name': 'regex', 'args': {'regex': r'\d+'}}
                ]
            },
            'second_field': {
                'type': 'string',
                'description': 'Some description',
                'nullable': True,
                'checks': [
                    'json'
                ]
            }
        }
    }
    schema = _yaml_parser.load_schema(raw_schema)

    with pytest.raises(errors.RecordValidationError) as err:
        schema.process({'first_field': 'foobar', 'second_field': 'fizz'})

    err_msg = 'value of "foobar" for first_field did not pass regex check'
    assert err_msg in str(err.value)
    err_msg = 'value of "fizz" for second_field did not pass json check'
    assert err_msg in str(err.value)


def test_load_schema_with_field_missing_key():
    """Should get an error if a required field key is missing."""
    with pytest.raises(errors.SchemaValidationError):
        _yaml_parser.load_schema({'name': 'foo', 'fields': {'bar': {}}})
