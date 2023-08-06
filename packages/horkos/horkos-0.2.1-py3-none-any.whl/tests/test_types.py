import typing

import pytest

from horkos import types
from horkos import errors


def test_str_less_aggressive():
    """The string caster in _casters should not aggressively cast to strings."""
    value = {'foo': 'bar'}

    with pytest.raises(errors.CastingError) as err:
        types._string(value)

    assert 'cannot unambiguously cast' in str(err.value)


SCENARIOS = [
    ('true', True),
    ('False', False),
    (0, False),
    (1, True),
    (True, True),
]

@pytest.mark.parametrize('value,expected', SCENARIOS)
def test_boolean(value: typing.Union[bool, str, int], expected: bool):
    """Should be able to cast value to booleans."""
    result = types._bool(value)

    assert result == expected
