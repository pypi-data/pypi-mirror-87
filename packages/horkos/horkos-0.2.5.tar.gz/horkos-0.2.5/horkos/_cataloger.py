import typing

from horkos import _yaml_parser
from horkos import _schemaomatic


class Catalog:
    """
    A collection of schemas.

    :param schemas:
        The schemas to include in the catalog.
    """

    def __init__(
            self,
            schemas: typing.List[_yaml_parser.Schemaable] = None,
    ):
        """Initialize the catalog of data schemas."""
        schemas = schemas or []
        all_schemas = [
            _yaml_parser.load_schema(s) for s in schemas
        ]
        self._schema_map = {s.name: s for s in all_schemas}
        if None in self._schema_map:
            raise ValueError('All schemas within a catalog must be named.')


    def process(
            self,
            name: str,
            record: dict,
    ) -> dict:
        """
        Process a record against a named schema from the catalog.

        Each field within the record will be cast to the type specified in
        the schema and the resulting value validated against the checks
        defined within the schema. If any of the fields
        cannot be successfully cast or any of the checks fail a
        RecordValidationError exception will be raised.

        :param name:
            The name of the schema to process the record against.
        :param record:
            The record to process against the schema. This should be
            a dictionary mapping field names to field values.
        :return:
            The processed record with values cast and validated.
        """
        schema = self._pull_schema(name)
        return schema.process(record)

    def _pull_schema(self, name: str) -> _schemaomatic.Schema:
        """
        Pull the schema with the given name, if no matching schema exists
        raise a value error indicating as much.
        """
        schema = self._schema_map.get(name)
        if schema is None:
            raise ValueError(f'No schema exists for "{name}"')
        return schema

    def update(self, schema: _yaml_parser.Schemaable):
        """
        Update the catalog with the given schema.

        :param schema:
            The schema to add/update to the catalog.
        """
        to_add = _yaml_parser.load_schema(schema)
        if to_add.name is None:
            raise ValueError('All schemas within a catalog must be named.')
        self._schema_map[to_add.name] = to_add

    @property
    def schemas(self) -> typing.List[_schemaomatic.Schema]:
        """All of the schemas contained within the catalog."""
        return list(self._schema_map.values())
