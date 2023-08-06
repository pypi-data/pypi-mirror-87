import dataclasses


@dataclasses.dataclass(frozen=True)
class Critique:
    """
    A critique of a dataschema.

    :vartype scope: str
    :ivar scope:
        The scope of the critique. A critique can be scoped as
        `schema`, `relative`, or `catalog` corresponding to
        whether it applies to a single schema, an addition of a schema
        to an existing catalog, or a catalog as a whole.
    :vartype code: str
    :ivar code:
        A short code identifying the critique.
    :vartype message: str
    :ivar message:
        A message describing the critique in detail.
    :vartype schema_name: str
    :ivar schema_name:
        The schema the critique is associated with.
    :vartype field_name: str
    :ivar field_name:
        The field the critique is associated with.
    """

    scope: str
    code: str
    message: str
    schema_name: str = None
    field_name: str = None

    def __str__(self):
        """Convert the critique to a string."""
        parts = [self.schema_name, self.field_name]
        parts = [p for p in parts if p is not None]
        name = '.'.join(parts)
        return f'[{self.code}] {name} - {self.message}'
