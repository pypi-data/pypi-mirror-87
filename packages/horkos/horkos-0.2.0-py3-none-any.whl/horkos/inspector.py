import typing


class CheckMetadata(typing.NamedTuple):
    """The name and args associated with a check."""

    name: str
    args: dict


def get_check_metadata(check: typing.Callable) -> CheckMetadata:
    """Get the metadata associated with a given check."""
    name = getattr(check, 'name', None) or getattr(check, '__name__')
    args = getattr(check, 'args', {})
    return CheckMetadata(name, args)
