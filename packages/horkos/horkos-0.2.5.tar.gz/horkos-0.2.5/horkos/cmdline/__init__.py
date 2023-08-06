import argparse

from horkos.cmdline import check
from horkos.cmdline import critique

_HANDLERS = {
    'check': check,
    'critique': critique,
}

def _parse(args: list = None) -> dict:
    """Parse the given arguments and return them as a simple dictionary."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    for name, handler in _HANDLERS.items():
        subparser = subparsers.add_parser(name, help=handler.__doc__)
        handler.configure_parser(subparser)
    return vars(parser.parse_args(args))


def main(args: list = None):
    """Run the horkos command."""
    parsed_args = _parse(args)
    command = parsed_args.pop('subcommand')
    _HANDLERS[command].main(**parsed_args)
