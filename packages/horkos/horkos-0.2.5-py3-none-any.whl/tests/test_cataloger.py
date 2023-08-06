import pytest

import horkos
from horkos import _cataloger


def test_catalog_process_happy_path():
    """Should be able to process a record through a catalog."""
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog = _cataloger.Catalog([schema])

    record = catalog.process('dataset', {'foo': 'bar'})

    assert record['foo'] == 'bar'


def test_catalog_process_sad_path():
    """Should be able to process a record through a catalog."""
    catalog = _cataloger.Catalog()

    with pytest.raises(ValueError) as err:
        catalog.process('doesnt-exist', {'foo': 'bar'})

    assert 'No schema exists for "doesnt-exist"' in str(err.value)


def test_catalog_update():
    """Should be able to update an existing catalog."""
    catalog = _cataloger.Catalog()
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog.update(schema)

    record = catalog.process('dataset', {'foo': 'bar'})

    assert record['foo'] == 'bar'


def test_catalog_requires_schema_names():
    """Every schema in a catalog should be required to have a name."""
    schema = horkos.Schema()

    with pytest.raises(ValueError):
        catalog = _cataloger.Catalog([schema])


def test_catalog_requires_schema_names_on_update():
    """
    When updating a schema in a catalog it should be required to have
    a name.
    """
    schema = horkos.Schema()
    catalog = _cataloger.Catalog()

    with pytest.raises(ValueError):
        catalog.update(schema)
