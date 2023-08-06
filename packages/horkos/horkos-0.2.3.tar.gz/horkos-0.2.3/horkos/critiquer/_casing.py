import collections
import itertools
import re
import typing


from horkos import _cataloger
from horkos.critiquer import _utils
from horkos.critiquer import _definitions
from horkos import _schemaomatic


CAMEL_REGEX = re.compile(r'^[a-z]+([A-Z][a-z]*)*$')
CAPS_REGEX = re.compile(r'^([A-Z]+_{0,1})*[A-Z]+$')
PASCAL_REGEX = re.compile(r'^([A-Z][a-z]*)+$')
SNAKE_REGEX = re.compile(r'^([a-z]+_{0,1})*[a-z]+$')
CASE_MAP = {
    'CAPS_CASE': CAPS_REGEX,
    'camelCase': CAMEL_REGEX,
    'PascalCase': PASCAL_REGEX,
    'snake_case': SNAKE_REGEX,
}


def _casing_type(value: str) -> list:
    """Determine which casing types the value adheres to."""
    return [case for case, regex in CASE_MAP.items() if regex.match(value)]


def _most_common_casing_type(values: typing.List[str]) -> typing.Tuple:
    """Identify the most common casing type from the list of strings."""
    counter = collections.Counter(
        itertools.chain.from_iterable(
            _casing_type(value) for value in values
        )
    )
    common = counter.most_common()
    if not common:
        return [], 0
    count = common[0][1]
    casings = [c for c in CASE_MAP if counter[c] == count]
    return casings, count


def schema_uniform_field_casing_check(
        schema: _schemaomatic.Schema
) -> typing.List[_definitions.Critique]:
    """Within a schema fields should have uniform casing."""
    casings, count = _most_common_casing_type(f.name for f in schema.fields)
    if count == len(schema.fields):
        return []
    verb = 'is' if len(casings) == 1 else 'are'
    suggestions = _utils.oxford_join(casings)
    closest = (
        ''
        if count == 0
        else f' {suggestions} {verb} most common with {count} matching.'
    )
    msg = f'No clear casing convention.{closest}'
    return [_definitions.Critique(
        'schema', 'field_consistency', msg, schema.name
    )]


@_utils.schema_not_in_catalog
def relative_field_casing_check(
        schema: _schemaomatic.Schema, catalog: _cataloger.Catalog
) -> typing.List[_definitions.Critique]:
    """
    When comparing a schema against a catalog the schema should have
    casing conventions that are consistent with the catalog.
    """
    fields = [f.name for s in catalog.schemas for f in s.fields]
    catalog_casings, catalog_count = _most_common_casing_type(fields)
    percentage = int(catalog_count * 100 / (len(fields) or 1))
    conventions = _utils.oxford_join(catalog_casings, last='or')
    non_existing = {f.name for f in schema.fields} - set(fields)
    critiques = []
    for field in non_existing:
        overlap = set(_casing_type(field)).intersection(catalog_casings)
        if overlap or not catalog_casings:
            continue
        msg = (
            f'The casing of {field} does not match the dominant '
            f'patterns of the catalog. {percentage}% of fields in the catalog '
            f'follow {conventions}.'
        )
        critiques.append(_definitions.Critique(
            'relative', 'field_consistency', msg, schema.name, field
        ))
    return critiques


def catalog_field_casing_check(
        catalog: _cataloger.Catalog
) -> typing.List[_definitions.Critique]:
    """
    Naming conventions should be consistent across all fields in a catalog.

    :param catalog:
        The group of schemas to check for uniformity.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    fields = [f.name for s in catalog.schemas for f in s.fields]
    casings, count = _most_common_casing_type(fields)
    if len(fields) == count:
        return []
    verb = 'is' if len(casings) == 1 else 'are'
    suggestions = _utils.oxford_join(casings)
    percentage = int(count * 100 / (len(fields) or 1))
    closest = (
        ''
        if count == 0
        else f' {suggestions} {verb} most common with {percentage}% matching.'
    )
    msg = f'No clear casing convention.{closest}'
    return [_definitions.Critique('catalog', 'field_consistency', msg)]


def schema_prefer_snake_case(
        schema: _schemaomatic.Schema
) -> typing.List[_definitions.Critique]:
    """
    snake_case should be the preferred.

    :param schema:
        The schema to validate for snake_case usage.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    casings, _ = _most_common_casing_type(f.name for f in schema.fields)
    if 'snake_case' in casings:
        return []
    joined = _utils.oxford_join(casings, last="or")
    current = (
        ''
        if not casings else
        f' Schema is currently using {joined}.'
    )
    msg = (
        'snake_case field names are recommended for the greatest '
        f'compatibility with common big data technologies.{current}'
    )
    return [
        _definitions.Critique(
            'schema', 'recommend_snake_case', msg, schema.name
        )
    ]


def catalog_prefer_snake_case(
        catalog: _cataloger.Catalog
) -> typing.List[_definitions.Critique]:
    """
    snake_case should be the preferred.

    :param catalog:
        The catalog to validate for snake_case usage.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    fields = [
        field.name
        for schema in catalog.schemas
        for field in schema.fields
    ]

    casings, _ = _most_common_casing_type(fields)
    if 'snake_case' in casings:
        return []
    joined = _utils.oxford_join(casings, last="or")
    current = (
        ''
        if not casings else
        f' Catalog is currently using {joined}.'
    )
    msg = (
        'snake_case field names are recommended for the greatest '
        f'compatibility with common big data technologies.{current}'
    )
    return [_definitions.Critique('catalog', 'recommend_snake_case', msg)]
