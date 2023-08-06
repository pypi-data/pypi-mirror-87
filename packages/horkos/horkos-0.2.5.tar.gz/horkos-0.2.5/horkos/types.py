# pylint: disable=broad-except
import functools
import typing

from horkos import errors


def _allow_nulls(func: typing.Callable) -> typing.Callable:
    """Create a function that immediately returns None if given None."""

    @functools.wraps(func)
    def wrapper(value: typing.Any) -> typing.Any:
        """Return None if None is given."""
        if value is None:
            return value
        return func(value)

    return wrapper


def _all_errors_to_casting_error(func: typing.Callable) -> typing.Callable:
    """Create a function that converts exceptions to casting errors."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Convert all exceptions to CastingErrors."""
        try:
            return func(*args, **kwargs)
        except errors.CastingError as err:
            raise err
        except Exception:
            raise errors.CastingError('cannot cast')

    return wrapper


@_all_errors_to_casting_error
@_allow_nulls
def _integer(value: typing.Any) -> int:
    """Convert the given value into an integer."""
    if isinstance(value, float) and (int(value) - value) != 0:
        raise errors.CastingError('cannot losslessly cast')
    return int(value)


@_all_errors_to_casting_error
@_allow_nulls
def _bool(value: typing.Any) -> bool:
    """Convert the given value to a boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() == 'true' or value == '1':
        return True
    if isinstance(value, str) and value.lower() == 'false' or value == '0':
        return False
    if isinstance(value, int) and value == 0:
        return False
    if isinstance(value, int) and value == 1:
        return True
    raise errors.CastingError('cannot unambiguously cast')


@_all_errors_to_casting_error
@_allow_nulls
def _float(value: typing.Any) -> float:
    """Convert the given value to a float"""
    return float(value)


@_all_errors_to_casting_error
@_allow_nulls
def _string(value: typing.Any) -> str:
    """Convert the given value to a string."""
    if isinstance(value, (str, int, float)):
        return str(value)
    raise errors.CastingError('cannot unambiguously cast')


class FieldType:
    """The base type for all field types."""

    name: str
    _caster: typing.Callable

    @classmethod
    def cast(cls, value: typing.Any):
        """Cast the incoming value to the desired type."""
        return cls._caster(value)


class Boolean(FieldType):
    """
    A value that is either true or false. :code:`boolean` fields will cast
    strings that case insensitively match :code:`"true"` or :code:`"false"`
    exactly to :code:`True` and :code:`False` respectively. It will cast
    integers :code:`0` and :code:`1` to :code:`False` and :code:`True`
    respectively.
    """
    name = 'boolean'
    _caster = _bool


class Float(FieldType):
    """
    A numerical value with decimal components. :code:`float` fields will cast
    integers, as well as float strings and integer strings to float values.
    """
    name = 'float'
    _caster = _float


class Integer(FieldType):
    """
    A whole number value. :code:`integer` fields will cast integer strings
    to integers, they will also cast float values to integers if there is no
    decimal component. Float values with decimal components will fail to
    cast to integers.
    """
    name = 'integer'
    _caster = _integer


class String(FieldType):
    """
    Any string value. :code:`horkos` will only cast values that can be cast
    unambiguously to a string such as integers and floats. Other values
    that have a string encoding in python will not be cast to a string if
    there isn't exactly one reasonable string encoding. Examples of this are
    booleans (since :code:`True`, :code:`TRUE`, and :code:`true` are all
    equally reasonable) or dictionaries (since :code:`{'foo': 'bar'}` and
    :code:`{"foo": "bar"}` are equally reasonable).
    """
    name = 'string'
    _caster = _string


ALL_TYPES = [Boolean, Float, Integer, String]
TYPE_MAP = {t.name: t for t in ALL_TYPES}
