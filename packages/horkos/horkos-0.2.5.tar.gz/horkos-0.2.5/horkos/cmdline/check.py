"""
Check that an incoming stream or file of data matches the declared
schema.
"""
import argparse
import csv
import io
import json
import sys
import typing

from horkos import errors
from horkos import _yaml_parser


def configure_parser(parser: argparse.ArgumentParser):
    """Configure the given parser to work for the check command."""
    parser.add_argument(
        '--schema', '-s',
        dest='schema_file',
        required=True,
        type=argparse.FileType('r'),
        help='The schema file describing the data.'
    )
    parser.add_argument(
        'datafile',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
    )


def _convert_to_records(contents: str) -> typing.List[dict]:
    """
    Convert a file's contents into a set of records. The contents are expected
    to be either a csv with a header of column names, a json list, or a
    set of json records seperated by a new line.

    :param contents:
        The contents of the file to parse.
    :return:
        A list of records from the file.
    """
    try:
        rows = json.loads(contents)
        if isinstance(rows, list):
            return rows
    except ValueError:
        pass
    try:
        rows = [json.loads(r) for r in contents.strip().split('\n')]
        if all(isinstance(r, dict) for r in rows):
            return rows
    except ValueError:
        pass
    reader = csv.DictReader(io.StringIO(contents))
    return [
        {k: v if v != '' else None for k, v in r.items()}
        for r in reader
    ]


def main(
        datafile: io.TextIOWrapper,
        schema_file: io.TextIOWrapper,
        **_,
):
    """Validate that the input file matches the given schema."""
    schema = _yaml_parser.load_schema(schema_file)
    contents = datafile.read()
    records = _convert_to_records(contents)
    error_count = 0
    for i, record in enumerate(records):
        try:
            schema.process(record)
        except errors.RecordValidationError as err:
            error_count += 1
            print(f'[Row {i}]: {err}', file=sys.stdout)
    msg = f'{error_count} error{"s" if error_count != 1 else ""} found'
    print(msg)
