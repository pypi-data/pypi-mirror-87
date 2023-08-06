import io
from unittest import mock

import pytest

from horkos.cmdline import critique


def test_expand_directories_with_nonexistent_file():
    """Should get a SystemExit if a given file doesn't exist."""
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stderr', new=output):
            critique._expand_directories(['not-a-real-file.yaml'])

    result = output.getvalue()
    assert 'ERROR: not-a-real-file.yaml does not exist.' in result


@mock.patch('os.path.exists', new=lambda x: True)
@mock.patch('os.path.isdir', new=lambda x: False)
def test_expand_directories_with_nonschema_file():
    """Should get a SystemExit if a given file doesn't exist."""
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stderr', new=output):
            critique._expand_directories(['not-a-schema.csv'])

    result = output.getvalue()
    assert 'ERROR: not-a-schema.csv is not a yaml or json file.' in result


def test_load_schemas_no_file():
    """Attempting to load a non-existent file should sys exit."""
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stderr', new=output):
            critique._load_schemas('not-a-real-file.yaml')

    result = output.getvalue()
    assert 'ERROR: not-a-real-file.yaml does not exist.' in result


@mock.patch('horkos.cmdline.critique._assemble_catalog')
@mock.patch('horkos.cmdline.critique._load_schemas')
def test_relative_critique_already_exists(
        _load_schemas: mock.MagicMock,
        _assemble_catalog: mock.MagicMock,
):
    """Should error if the catalog already has a schema of the same name."""
    schema = mock.MagicMock()
    schema.name = 'foobar'
    _load_schemas.return_value = [schema]
    catalog = _assemble_catalog.return_value
    catalog.schemas = {'foobar': None}
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stderr', new=output):
            critique._relative_critique('schema_file', ['catalog_files'])

    result = output.getvalue()
    assert 'A schema named foobar is already in the catalog' in result
