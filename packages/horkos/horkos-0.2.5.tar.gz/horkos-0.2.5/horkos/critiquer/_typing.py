import collections
import typing

from horkos import _cataloger
from horkos.critiquer import _definitions
from horkos.critiquer import _utils
from horkos import _schemaomatic


@_utils.schema_not_in_catalog
def relative_type_consistency_check(
        schema: _schemaomatic.Schema, catalog: _cataloger.Catalog
) -> typing.List[_definitions.Critique]:
    """
    When comparing a schema against a catalog the schema's fields should have
    a typing consistent with the typing that already exists in the catalog.
    """
    fields = [f for schema in catalog.schemas for f in schema.fields]
    type_map = collections.defaultdict(set)
    for field in fields:
        type_map[field.name].add(field.type.name)
    critiques = []
    for field in schema.fields:
        consistent_type = field.type.name in type_map[field.name]
        if field.name not in type_map or consistent_type:
            continue
        types = list(sorted(type_map[field.name]))
        types_str = _utils.oxford_join(types, last='or')
        msg = (
            f'{field.name} declared as {field.type.name}, but other schemas '
            f'in the catalog have it declared as {types_str}. '
            f'The type of {field.name} should be consistent between schemas.'
        )
        critiques.append(_definitions.Critique(
            'relative', 'type_consistency', msg, schema.name, field.name
        ))
    return critiques

def catalog_type_consistency_check(
        catalog: _cataloger.Catalog
) -> typing.List[_definitions.Critique]:
    """
    Field types should be consistent within the catalog.

    :param catalog:
        The group of schemas to check for type uniformity.
    :return:
        A list of _definitions.Critiques .
    """
    fields = [f for schema in catalog.schemas for f in schema.fields]
    type_map = collections.defaultdict(set)
    for field in fields:
        type_map[field.name].add(field.type.name)
    return [
        _definitions.Critique(
            'catalog',
            'type_consistency',
            (
                f'Catalog describes {field.name} as '
                f'{_utils.oxford_join(list(sorted(type_map[field.name])))}. '
                f'The type of {field.name} should be consistent between '
                'schemas.'
            ),
            schema.name,
            field.name
        )
        for schema in catalog.schemas
        for field in schema.fields
        if len(type_map[field.name]) > 1
    ]
