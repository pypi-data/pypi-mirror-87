from unittest import mock

import pytest

import horkos
from horkos.critiquer import _casing


def test_schema_uniform_field_casing_check_with_critique():
    """Should identify mixed casing conventions within schema"""
    schema = horkos.load_schema({
        'name': 'ds1',
        'fields': {
            'fooBar': {'type': 'integer'}, 'fiz_buzz': {'type': 'integer'}
        }
    })

    result = _casing.schema_uniform_field_casing_check(schema)

    assert result
    expected = 'camelCase and snake_case are most common with 1 matching.'
    assert expected in result[0].message


def test_schema_uniform_field_casing_check_without_critique():
    """Should return none if the casing is consistent"""
    schema = horkos.load_schema({
        'name': 'ds1',
        'fields': {
            'foobar': {'type': 'integer'}, 'fiz_buzz': {'type': 'integer'}
        }
    })

    result = _casing.schema_uniform_field_casing_check(schema)

    assert not result


def test_relative_field_casing_check_with_critique():
    """Should identify mixed field conventions between schema and catalog."""
    field = {'type': 'integer'}
    foo_schema = horkos.load_schema({
        'name': 'foo',
        'fields': {'fooBar': field, 'fiz_buzz': field}
    })
    baz_schema = horkos.load_schema({
        'name': 'baz',
        'fields': {'fooBar': field, 'boo_far': field, 'biz_fuzz': field}
    })
    catalog = horkos.Catalog([foo_schema, baz_schema])
    schema = horkos.load_schema({'name': 'baz', 'fields': {'bizFuzz': field}})

    result = _casing.relative_field_casing_check(schema, catalog)

    assert result
    expected = (
        'The casing of bizFuzz does not match the dominant patterns of the '
        'catalog'
    )
    assert expected in result[0].message


def test_relative_field_casing_check_with_schema_in_catalog():
    """If the schema is already in the catalog an error should be raised."""
    catalog = mock.MagicMock(schemas={'foo': 'bar'})
    schema = mock.MagicMock()
    schema.name = 'foo'

    with pytest.raises(ValueError):
        _casing.relative_field_casing_check(schema, catalog)


def test_relative_field_casing_without_critique():
    """Should return None if their are no issues."""
    foobar_field = mock.MagicMock()
    foobar_field.name = 'fooBar'
    fizbuzz_field = mock.MagicMock()
    fizbuzz_field.name = 'fizBuzz'
    boofar_field = mock.MagicMock()
    boofar_field.name = 'booFar'
    bizfuzz_field = mock.MagicMock()
    bizfuzz_field.name = 'bizFuzz'
    catalog = mock.MagicMock(
        schemas=[
            mock.MagicMock(fields=[foobar_field, fizbuzz_field]),
            mock.MagicMock(fields=[foobar_field, boofar_field, bizfuzz_field]),
        ]
    )
    schema = mock.MagicMock(fields=[foobar_field, bizfuzz_field])

    result = _casing.relative_field_casing_check(schema, catalog)

    assert not result


def test_catalog_field_casing_check_with_critique():
    """Should be able to identify inconsistent naming in a catalog of data."""
    field = {'type': 'integer'}
    schemas = [
        horkos.load_schema({
            'name': 'foo',
            'fields': {'fooBar': field, 'fiz_buzz': field}
        }),
        horkos.load_schema({
            'name': 'baz',
            'fields': {'fooBar': field, 'boo_far': field, 'biz_fuzz': field}
        }),
    ]
    catalog = horkos.Catalog(schemas)

    result = _casing.catalog_field_casing_check(catalog)

    assert result
    expected = (
        'No clear casing convention. snake_case is most '
        'common with 60% matching.'
    )
    assert expected in result[0].message


def test_catalog_field_casing_check_without_critique():
    """Should return None if all fields are consistent."""
    field = {'type': 'integer'}
    schemas = [
        horkos.load_schema({
            'name': 'foo',
            'fields': {'foobar': field, 'fiz_buzz': field}
        }),
        horkos.load_schema({
            'name': 'baz',
            'fields': {'foobar': field, 'boo_far': field, 'biz_fuzz': field}
        }),
    ]
    catalog = horkos.Catalog(schemas)

    result = _casing.catalog_field_casing_check(catalog)

    assert not result


def test_schema_prefer_snake_case_with_critique():
    """
    Should be able to identify when snake_case isn't used in a schema
    and recommend its usage.
    """
    field = {'type': 'integer'}
    schema = horkos.load_schema({
        'name': 'foo',
        'fields': {'fooBar': field, 'fizBuzz': field}
    })

    result = _casing.schema_prefer_snake_case(schema)

    assert result
    expected = 'snake_case field names are recommended'
    assert expected in result[0].message


def test_schema_prefer_snake_case_without_critique():
    """If snake_case is already used, then return None."""
    field = {'type': 'integer'}
    schema = horkos.load_schema({
        'name': 'foo',
        'fields': {'foobar': field, 'fiz_buzz': field}
    })

    result = _casing.schema_prefer_snake_case(schema)

    assert not result


def test_catalog_prefer_snake_case_with_critique():
    """
    Should be able to identify when snake_case isn't used in a schema
    and recommend its usage.
    """
    field = {'type': 'integer'}
    schemas = [
        horkos.load_schema({
            'name': 'foo',
            'fields': {'Foobar': field, 'fiz_buzz': field}
        }),
        horkos.load_schema({
            'name': 'baz',
            'fields': {'Foobar': field, 'BooFar': field, 'biz_fuzz': field}
        }),
    ]
    catalog = horkos.Catalog(schemas)

    result = _casing.catalog_prefer_snake_case(catalog)

    assert result
    expected = 'snake_case field names are recommended'
    assert expected in result[0].message


def test_catalog_prefer_snake_case_without_critique():
    """If snake_case is already used, then return None."""
    field = {'type': 'integer'}
    schemas = [
        horkos.load_schema({
            'name': 'foo',
            'fields': {'foobar': field, 'fiz_buzz': field}
        }),
        horkos.load_schema({
            'name': 'baz',
            'fields': {'foobar': field, 'boo_far': field}
        }),
    ]
    catalog = horkos.Catalog(schemas)

    result = _casing.catalog_prefer_snake_case(catalog)

    assert not result


def test_most_common_casing_type_when_empty():
    """If empty an empty list should be returned."""
    values = ['foo_Bar-baz']

    result = _casing._most_common_casing_type(values)

    assert not result[0]
    assert result[1] == 0
