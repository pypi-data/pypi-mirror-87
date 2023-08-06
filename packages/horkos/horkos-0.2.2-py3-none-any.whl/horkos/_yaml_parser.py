import functools
import inspect
import typing
import yaml

from horkos import checks as hs_checks
from horkos import errors
from horkos import _fields
from horkos import _schemaomatic
from horkos import types

Schemaable = typing.Union[str, dict, _schemaomatic.Schema, typing.TextIO]


def _schema_from_dict(
        raw_schema: dict,
        custom_checkers: typing.Dict[str, typing.Callable] = None
) -> _schemaomatic.Schema:
    """
    Create a schema from a raw schema dictionary.

    :param raw_schema:
        A raw schema matching the expected json/yaml schema format.
    :param custom_checkers:
        A dictionary of custom checkers. This dictionary should map the name
        of the check to a function that generates the check function
    :return:
        The resulting schema.
    """
    standardized = _standardize_schema(raw_schema)
    check_map = hs_checks.CHECK_MAP.copy()
    check_map.update(custom_checkers or {})
    fields = []
    raw_fields = standardized['fields']
    for field_name, field_body in raw_fields.items():
        field_checks = []
        for i, raw_check in enumerate(field_body['checks']):
            position = f'fields.{field_name}.checks[{i}]'
            check_name = raw_check['name']
            if check_name not in check_map:
                raise errors.SchemaValidationError(
                    f'In "{position}" check name "{check_name}" is unknown.'
                )
            check = _create_check_func(
                check_map[check_name],
                raw_check['args'],
                position
            )
            field_checks.append(check)
        fields.append(_fields.Field(
            field_name,
            types.TYPE_MAP[field_body['type']],
            field_body['description'],
            field_body['required'],
            field_body['nullable'],
            field_checks,
            field_body['labels'],
        ))
    return _schemaomatic.Schema(
        standardized['name'],
        standardized['description'],
        standardized['labels'],
        fields,
    )

def _load_yaml(
        filepath_or_handle: typing.Union[str, typing.TextIO]
) -> dict:
    """
    Read the given yaml file.

    :param filepath_or_handle:
        The path to the yaml file to convert into a schema.
    :return:
        The resulting schema.
    """
    if not isinstance(filepath_or_handle, str):
        return yaml.safe_load(filepath_or_handle)
    with open(filepath_or_handle) as f:
        return yaml.safe_load(f)


def _create_check_func(
        check: typing.Callable, args: dict, position: str
) -> typing.Callable:
    """
    Create the actual check function, baking the args into it. The returned
    function should only expect a single positional argument to check.

    :param check:
        The base check. This is either a class that will be initialized
        with the given arguments, or a function that will be partially filled
        with the given args.
    :param args:
        The arguments to initialize the check with.
    :param position:
        The position of the check within the schema. This is used to provide
        more clear error messages.
    :return:
        A callable that expects a single positional argument that it will
        check.
    """
    try:
        if inspect.isclass(check):
            return check(**args)
        signature = inspect.signature(check)
        signature.bind('value', **args)
    except TypeError:
        raise errors.SchemaValidationError(
            f'Invalid arguments in "{position}"'
        )
    return functools.partial(check, **args)


def _standardize_schema(raw_schema: dict) -> dict:
    """
    Standardize the given raw_schema with all optional fields filled out
    with defaults. If the raw schema is not valid a SchemaValidationError will
    be raised.

    :param raw_schema:
        The schema to standardize.
    :return:
        The standardized schema.
    """
    standardized = {}
    top = [
        ('name', str, True),
        ('description', str, False),
        ('labels', dict, False),
        ('fields', dict, False),
    ]
    for key, type_, required in top:
        if key not in raw_schema and required:
            raise errors.SchemaValidationError(f'"{key}" is required')
        value = raw_schema[key] if key in raw_schema else type_()
        if not isinstance(value, type_):
            raise errors.SchemaValidationError(
                f'"{key}" must be of type {type_.__name__}'
            )
        standardized[key] = value
    standardized['fields'] = {
        field_id: _standardize_field(raw_field, field_id)
        for field_id, raw_field in raw_schema['fields'].items()
    }
    return standardized


def _standardize_field(raw_field: dict, field_id: str) -> dict:
    """
    Standardize a given raw field with all the optional parts filled out
    with defaults. If the raw field can't be validated a SchemaValidationError
    will be raised.

    :param raw_field:
        The raw field to standardize.
    :param field_id:
        The id of the field being standardized.
    :return:
        The standardized field.
    """
    standardized = {}
    top = [
        ('type', str, True, None),
        ('description', str, False, str),
        ('labels', dict, False, dict),
        ('checks', list, False, list),
        ('required', bool, False, lambda: True),
        ('nullable', bool, False, bool),
    ]
    for key, type_, required, default in top:
        working = f'fields.{field_id}.{key}'
        if key not in raw_field and required:
            raise errors.SchemaValidationError(f'"{working}" is required')
        value = raw_field[key] if key in raw_field else default()
        if not isinstance(value, type_):
            raise errors.SchemaValidationError(
                f'"{working}" must be of type {type_.__name__}'
            )
        standardized[key] = value
    standardized['checks'] = [
        _standardize_check(raw_check, f'fields.{field_id}.check[{i}]')
        for i, raw_check in enumerate(raw_field.get('checks') or [])
    ]
    return standardized


def _standardize_check(
        raw_check: typing.Union[str, dict], prefix: str
) -> dict:
    """
    Convert a check into the standard format. If the check cannot be
    standardize a schema validation error is raised.

    :param raw_check:
        The raw_check to standardize.
    :param prefix:
        The document position prefix to integrate into error messages.
    :return:
        A standard check dictionary.
    """
    if isinstance(raw_check, str):
        return {'name': raw_check, 'args': {}}
    if isinstance(raw_check, dict):
        if 'name' not in raw_check:
            raise errors.SchemaValidationError(
                f'"{prefix}.name" is required'
            )
        if not isinstance(raw_check['name'], str):
            raise errors.SchemaValidationError(
                f'"{prefix}.name" must be a string'
            )
        if 'args' in raw_check and not isinstance(raw_check['args'], dict):
            raise errors.SchemaValidationError(
                f'"{prefix}.args" must be a dictionary'
            )
        return {'name': raw_check['name'], 'args': raw_check.get('args', {})}
    raise errors.SchemaValidationError(
        f'"{prefix}" must be a string or dictionary'
    )


def load_schema(
        schema: Schemaable,
        custom_checkers: typing.Dict[str, typing.Callable] = None
) -> _schemaomatic.Schema:
    """
    Load a schema from a file or existing schema object.

    :param schema:
        The schema to load. If a string is given, it is assumed to be a path
        to a `.json` or `.yaml` file defining the schema, alternatively a file
        handle can be passed directly. If a dictionary is given it will be
        assumed to be equivalent to the contents of a schema file.
    :param custom_checkers:
        A dictionary of custom checkers. This dictionary should map the name
        of the check to a function that generates the check function. This
        can be used to extend checks beyond those defined within `horkos`.
    :return:
        A Schema object.
    """
    working = schema
    custom_checkers = custom_checkers or {}
    if isinstance(working, _schemaomatic.Schema):
        return working
    if not isinstance(working, dict):
        working = _load_yaml(working)
    return _schema_from_dict(
        working, custom_checkers=custom_checkers
    )
