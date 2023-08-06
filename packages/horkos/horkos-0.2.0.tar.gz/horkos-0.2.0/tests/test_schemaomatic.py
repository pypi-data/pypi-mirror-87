import os
import typing

import pytest

import horkos
from horkos import errors
from horkos import _schemaomatic
from horkos import types


def test_process_raises_all_casting_errors():
    """Should raise all errors when present."""
    fields = [
        horkos.Field('bool_field', types.Boolean),
        horkos.Field('float_field', types.Float),
        horkos.Field('int_field_1', types.Integer),
        horkos.Field('int_field_2', types.Integer),
        horkos.Field('str_field', types.String),
    ]
    schema = _schemaomatic.Schema(fields=fields)
    record = {
        'bool_field': 'T',
        'float_field': 'word',
        'int_field_1': 1.123,
        'int_field_2': 'word',
        'str_field': None,
    }

    with pytest.raises(errors.RecordValidationError) as err:
        schema.process(record)

    msg = 'cannot unambiguously cast T to boolean in bool_field'
    assert msg in str(err.value)
    msg = 'cannot cast word to float in float_field'
    assert msg in str(err.value)
    msg = 'cannot losslessly cast 1.123 to integer in int_field_1'
    assert msg in str(err.value)
    msg = 'cannot cast word to integer in int_field_2'
    assert msg in str(err.value)


def test_schema_with_repeated_fields():
    """Repeated fields of the same name should raise an error."""
    field = horkos.Field('field_name', types.Boolean)

    with pytest.raises(ValueError):
        _schemaomatic.Schema(fields=[field, field])
