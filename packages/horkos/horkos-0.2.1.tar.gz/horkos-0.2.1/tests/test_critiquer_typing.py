from unittest import mock

import horkos
from horkos.critiquer import _typing


def test_catalog_type_consistency_check_with_critique():
    """The types of each field should be consistent across schemas."""
    schema_1 = horkos.load_schema({
        'name': 'ds1', 'fields': {'foobar': {'type': 'integer'}}
    })
    schema_2 = horkos.load_schema({
        'name': 'ds2', 'fields': {'foobar': {'type': 'string'}}
    })
    catalog = horkos.Catalog([schema_1, schema_2])

    result = _typing.catalog_type_consistency_check(catalog)

    assert result
    expected = (
        'Catalog describes foobar as integer and string. The type of foobar '
        'should be consistent between schemas.'
    )
    assert expected in result[0].message


def test_catalog_type_consistency_check_without_critique():
    """If types are consistent then no critique should be returned."""
    schema_1 = horkos.load_schema({
        'name': 'ds1', 'fields': {'foobar': {'type': 'integer'}}
    })
    schema_2 = horkos.load_schema({
        'name': 'ds2', 'fields': {'foobar': {'type': 'integer'}}
    })
    catalog = horkos.Catalog([schema_1, schema_2])

    result = _typing.catalog_type_consistency_check(catalog)

    assert not result


def test_relative_type_consistency_check_with_critique():
    """The types of a new schema should be consistent with existing"""
    schema = horkos.load_schema({
        'name': 'ds1', 'fields': {'foobar': {'type': 'integer'}}
    })
    catalog = horkos.Catalog([schema])
    new_schema = horkos.load_schema({
        'name': 'ds2', 'fields': {'foobar': {'type': 'string'}}
    })

    result = _typing.relative_type_consistency_check(new_schema, catalog)

    assert result
    expected = 'other schemas in the catalog have it declared as integer'
    assert expected in result[0].message


def test_relative_type_consistency_check_without_critique():
    """If types are consistent, then no critiques should be raised."""
    schema = horkos.load_schema({
        'name': 'ds1', 'fields': {'foobar': {'type': 'integer'}}
    })
    catalog = horkos.Catalog([schema])
    new_schema = horkos.load_schema({
        'name': 'ds2', 'fields': {'foobar': {'type': 'integer'}}
    })

    result = _typing.relative_type_consistency_check(new_schema, catalog)

    assert not result
