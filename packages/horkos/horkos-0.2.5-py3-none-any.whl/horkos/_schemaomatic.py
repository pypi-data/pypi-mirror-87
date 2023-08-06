import collections
import typing

from horkos import errors
from horkos import inspector
from horkos import _fields


class Schema:
    """
    A formal specification of a dataset. It defines all fields (or columns) a
    dataset is expected to have as well as the properties of each field.

    :vartype name: str
    :ivar name:
        The name of the dataset defined by the schema.
    :vartype name: str
    :ivar description:
        A detailed description of the dataset defined by the schema.
    :vartype labels: dict
    :ivar labels:
        A dictionary of key value pairs containing organization
        specific structured information about the dataset. These values have
        no function within `horkos`.
    :vartype fields: typing.List[horkos.Field]
    :ivar fields:
        A list of fields expected within the dataset.
    :param name:
        The name of the dataset described by the schema. This is used to
        provide more descriptive error messages and to provide an identity
        while being used as part of a Catalog.
    :param description:
        A detailed description of the dataset defined by the schema.
    :param labels:
        A dictionary of minimally structured key value pairs intended for
        storing organization specific information relating to the dataset.
    :param fields:
        A list of fields (or columns) that are expected within the dataset.
        Each field must have its own unique name.
    """

    def __init__(
            self,
            name: str = None,
            description: str = None,
            labels: dict = None,
            fields: typing.List[_fields.Field] = None,
    ):
        """Class constructor."""
        self.name = name
        self.description = description
        self.labels = dict(labels or {})
        fields = fields or []
        common = collections.Counter(f.name for f in fields).most_common(1)
        if common and common[0][1] > 1:
            msg = (
                f'Field named "{common[0][0]}" appears {common[0][1]} times.'
                ' Field names should be unique within a schema.'
            )
            raise ValueError(msg)
        self.fields = list(fields)

    def _cast(self, record: dict) -> dict:
        """
        Cast all the values contained within the record to the types declared
        within the schema, removing all undeclared fields from the record.

        :param record:
            A dictionary mapping field names to field values.
        :return:
            The record with values cast to the declared types.
        """
        error_list = []
        cast = {}
        for field in self.fields:
            try:
                value = record.get(field.name)
                cast[field.name] = field.type.cast(value)
            except errors.CastingError as err:
                error_list.append(
                    f'{str(err)} {value} to {field.type.name} in {field.name}'
                )
        if error_list:
            msg = f'Casting failed: {", ".join(error_list)}'
            raise errors.RecordValidationError(msg)
        return cast

    def _apply_checks(self, record: dict):
        """
        Apply field checks to the incoming record, raising an error if
        any of them fail.
        """
        error_list = []
        for field in self.fields:
            value = record[field.name]
            if value is None:
                continue
            for check in field.checks:
                if not check(value):
                    expanded = inspector.get_check_metadata(check)
                    error_list.append(
                        f'value of "{value}" for {field.name} did not pass '
                        f'{expanded.name} check'
                    )
        if error_list:
            msg = f'Checks failed: {", ".join(error_list)}'
            raise errors.RecordValidationError(msg)

    def process(self, record: dict) -> dict:
        """
        Process a record against the schema. This process includes:

            1. Confirming all required fields are present.
            2. Casting all field values to their expected type.
            3. Confirming there are no null values in non-nullable fields.
            4. Confirm all non-null values pass their field's checks.

        The cast and validated record is returned.

        :param record:
            A dictionary mapping field names to field values.
        :return:
            The processed record with values cast and validated.
        """
        missing_fields = [
            f.name for f in self.fields if f.required and f.name not in record
        ]
        if missing_fields:
            msg = f'Required fields are missing: {", ".join(missing_fields)}'
            raise errors.RecordValidationError(msg)

        cast = self._cast(record)

        null_fields = [
            f.name
            for f in self.fields if not f.nullable and cast[f.name] is None
        ]
        if null_fields:
            msg = f'Non-nullable fields are null: {", ".join(null_fields)}'
            raise errors.RecordValidationError(msg)

        self._apply_checks(cast)
        return cast
