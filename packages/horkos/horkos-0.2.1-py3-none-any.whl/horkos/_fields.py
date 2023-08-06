import typing

from horkos import types


class Field:
    """
    The definition of a field within a schema.

    :vartype name: str
    :ivar name:
        The name of the field.
    :vartype type: types.FieldType
    :ivar type:
        The type of the field.
    :vartype description: str
    :ivar description:
        A detailed description of the field.
    :vartype required: bool
    :ivar required:
        Whether the field is required to be present.
    :vartype nullable: bool
    :ivar nullable:
        Whether the field should accept null values.
    :vartype checks: typing.List[typing.Callable]
    :ivar checks:
        A list of callables accepting a single value to validate.
    :vartype labels: dict
    :ivar labels:
        A space for unstructured information regarding the field.
    """

    def __init__(
            self,
            name: str,
            type_: types.FieldType,
            description: str = None,
            required: bool = True,
            nullable: bool = False,
            checks: typing.List[typing.Callable] = None,
            labels: dict = None,
    ):
        """Constructor for field."""
        self.name = name
        self.type = type_
        self.description = description
        self.required = required
        self.nullable = nullable
        self.checks = checks or []
        self.labels = labels or []
