import functools
import typing

from horkos import _schemaomatic
from horkos import _cataloger


def oxford_join(values: typing.List[str], last: str = 'and') -> str:
    """Join the given strings into an english list."""
    if not values:
        return ''
    if len(values) == 1:
        return values[0]
    working = values.copy()
    working[-1] = f'{last} {working[-1]}'
    joiner = ', ' if len(values) > 2 else ' '
    return joiner.join(working)


def schema_not_in_catalog(func: typing.Callable) -> typing.Callable:
    """
    Decorate a relative critique function to require a schema is not in
    the given catalog.
    """

    @functools.wraps(func)
    def wrapper(
            schema: _schemaomatic.Schema,
            catalog: _cataloger.Catalog,
            *args,
            **kwargs,
    ):
        """Require that the schema is not in the catalog."""
        if schema.name in catalog.schemas:
            raise ValueError(f'schema named {schema.name} already in catalog.')
        return func(schema, catalog, *args, **kwargs)
    return wrapper
