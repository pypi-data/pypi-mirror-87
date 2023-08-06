"""
Critique a schema or catalog of schemas. This identifies common mistakes in
field design and potential issues between schemas within a catalog.
"""
import argparse
import os
from os import path
import re
import sys
import typing

import yaml

from horkos import _cataloger
from horkos import critiquer
from horkos import _schemaomatic
from horkos import _yaml_parser

SCHEMA_FILE_RE = re.compile(r'.*\.(yaml|yml|json)$')


def configure_parser(parser: argparse.ArgumentParser):
    """Configure the given parser to work for the critique command."""
    parser.add_argument(
        '--schema', '-s',
        dest='schema_file',
        help='The schema file to critique.'
    )
    parser.add_argument(
        '--catalog', '-c',
        action='append',
        dest='catalog_files',
        help=(
            'A path defining the catalog of schemas. If a directory is given '
            'all yaml files contained within will be used as schemas in the '
            'catalog. If used without the `--schema` flag the catalog itself '
            'will be critiqued, otherwise the flagged schema will be '
            'critiqued within the context of the given catalog.'
        )
    )


def _expand_directories(file_paths: typing.List[str]) -> typing.List[str]:
    """
    Expand any directories in the given set of paths replacing them with all
    of the yaml files they contain.
    """
    result = []
    for file_path in file_paths:
        if not path.exists(file_path):
            print(f'ERROR: {file_path} does not exist.', file=sys.stderr)
            sys.exit(1)
        if not path.isdir(file_path):
            if not SCHEMA_FILE_RE.match(file_path):
                print(
                    f'ERROR: {file_path} is not a yaml or json file.',
                    file=sys.stderr
                )
                sys.exit(1)
            result.append(file_path)
            continue
        for root, _, files in os.walk(file_path):
            result.extend(
                path.abspath(path.join(root, f))
                for f in files
                if SCHEMA_FILE_RE.match(f)
            )
    return result


def _load_schemas(schema_file: str) -> typing.List[_schemaomatic.Schema]:
    """Load the given schema file returnings all schemas it contains."""
    if not path.isfile(schema_file):
        print(f'ERROR: {schema_file} does not exist.', file=sys.stderr)
        sys.exit(1)
    with open(schema_file) as f:
        contents = f.read()
    return [
        _yaml_parser.load_schema(doc) for doc in yaml.safe_load_all(contents)
    ]


def _assemble_catalog(catalog_files: typing.List[str], omit: str = None):
    """Assemble a catalog using the given catalog files."""
    if omit in catalog_files:
        print(
            f'ERROR: {omit} is given for both --schema and --catalog',
            file=sys.stderr,
        )
        sys.exit(1)
    expanded_catalog = set(_expand_directories(catalog_files))
    if omit:
        expanded_catalog -= {path.abspath(omit)}
    catalog = _cataloger.Catalog()
    for file_path in expanded_catalog:
        with open(file_path) as f:
            contents = f.read()
        for doc in yaml.safe_load_all(contents):
            catalog.update(doc)
    return catalog


def _schema_critique(schema_file: str) -> typing.List[critiquer.Critique]:
    """Critique a schema."""
    critiques = []
    for schema in _load_schemas(schema_file):
        critiques.extend(critiquer.critique_schema(schema))
    return critiques


def _relative_critique(
        schema_file: str, catalog_files: typing.List[str]
) -> typing.List[critiquer.Critique]:
    """Critique the schema within the context of the catalog."""
    schemas = _load_schemas(schema_file)
    catalog = _assemble_catalog(catalog_files, omit=schema_file)
    for schema in schemas:
        if schema.name not in catalog.schemas:
            continue
        print(
            f'A schema named {schema.name} is already in the catalog',
            file=sys.stderr,
        )
        sys.exit(1)
    critiques = []
    for schema in _load_schemas(schema_file):
        critiques.extend(critiquer.critique_addition(schema, catalog))
    return critiques


def _catalog_critique(
        catalog_files: typing.List[str]
) -> typing.List[critiquer.Critique]:
    """Critique the catalog."""
    catalog = _assemble_catalog(catalog_files)
    return critiquer.critique_catalog(catalog)


def main(
        schema_file: str,
        catalog_files: typing.List[str],
        **_,
):
    """Critique the given schema / catalog."""
    if not schema_file and not catalog_files:
        print('--schema or --catalog must be specified', file=sys.stderr)
        sys.exit(1)
    if schema_file and not catalog_files:
        critiques = _schema_critique(schema_file)
    if schema_file and catalog_files:
        critiques = _relative_critique(schema_file, catalog_files)
    if not schema_file and catalog_files:
        critiques = _catalog_critique(catalog_files)
    for critique in critiques:
        print(critique)
    if critiques:
        sys.exit(1)
