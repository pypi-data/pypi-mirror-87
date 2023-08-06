import typing

from horkos import _cataloger
from horkos import _schemaomatic
from horkos.critiquer._definitions import Critique
from horkos.critiquer import _casing
from horkos.critiquer import _typing


_CATALOG_CRITIQUERS = [
    _casing.catalog_prefer_snake_case,
    _casing.catalog_field_casing_check,
    _typing.catalog_type_consistency_check,
]
_RELATIVE_CRITIQUERS = [
    _casing.relative_field_casing_check,
    _typing.relative_type_consistency_check,
]
_SCHEMA_CRITIQUERS = [
    _casing.schema_prefer_snake_case,
    _casing.schema_uniform_field_casing_check,
]


def critique_addition(
        schema: _schemaomatic.Schema,
        catalog: _cataloger.Catalog,
) -> typing.List[Critique]:
    """
    Critique a schema within the context of adding it to the given catalog
    of schemas.

    :param schema:
        The schema to critique.
    :param catalog:
        The catalog of schemas it is being added to.
    :return:
        A list of critiques of the schema in the context of the catalog.
    """
    result = []
    for critiquer in _RELATIVE_CRITIQUERS:
        result.extend(critiquer(schema, catalog))
    return result


def critique_catalog(
        catalog: _cataloger.Catalog
) -> typing.List[Critique]:
    """
    Critique the schemas within the catalog as a cohesive group.

    :param catalog:
        The catalog to critique.
    :return:
        A list of critiques of the catalog.
    """
    result = []
    for critiquer in _CATALOG_CRITIQUERS:
        result.extend(critiquer(catalog))
    return result


def critique_schema(
        schema: _schemaomatic.Schema
) -> typing.List[Critique]:
    """
    Critique a specific schema for self contained issues.

    :param schema:
        The schema to critique.
    :return:
        A list of critiques of the schema.
    """
    result = []
    for critiquer in _SCHEMA_CRITIQUERS:
        result.extend(critiquer(schema))
    return result


__all__ = (
    'critique_addition', 'critique_catalog', 'critique_schema', 'Critique'
)
