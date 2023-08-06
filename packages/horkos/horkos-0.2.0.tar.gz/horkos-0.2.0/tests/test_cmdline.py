import io
import os
from unittest import mock

import pytest

from horkos import cmdline

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(DIR_PATH, 'resources')


def test_check_cmdline():
    """Check cmdline should be able to run."""
    schema_file = os.path.join(RESOURCE_PATH, 'sample.yaml')
    data_file = os.path.join(RESOURCE_PATH, 'sample.csv')
    output = io.StringIO()

    with mock.patch('sys.stdout', new=output):
        cmdline.main(['check', '--schema', schema_file, data_file])

    result = output.getvalue()
    assert 'value of "ERROR" for method did not pass choice check' in result
    expected = 'cannot cast BAD to integer in response_code'
    assert expected in result
    assert '2 errors found' in result


def test_critique_cmdline_relative():
    """Critique cmdline should be able to run a relative comparison."""
    schema_file = os.path.join(RESOURCE_PATH, 'sample.yaml')
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout', new=output):
            cmdline.main([
                'critique', '--schema', schema_file, '--catalog', RESOURCE_PATH
            ])

    result = output.getvalue()
    expected = '[field_consistency] http_request.response_code'
    assert expected in result
    expected = r'100% of fields in the catalog follow camelCase.'
    assert expected in result


def test_critique_cmdline_schema():
    """Critique cmdline should be able to run on a schema."""
    schema_file = os.path.join(RESOURCE_PATH, 'alternative.yaml')
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout', new=output):
            cmdline.main(['critique', '--schema', schema_file])

    result = output.getvalue()
    expected = '[recommend_snake_case] business-card - snake_case field names'
    assert expected in result


def test_critique_cmdline_catalog():
    """Critique cmdline should be able to run a catalog critique."""
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout', new=output):
            cmdline.main([
                'critique',
                '--catalog', RESOURCE_PATH,
                '--catalog', os.path.join(RESOURCE_PATH, 'sample.yaml')
            ])

    result = output.getvalue()
    expected = '[field_consistency]  - No clear casing convention.'
    assert expected in result


def test_critique_cmdline_catalog_no_flags():
    """Should get a bad error if we don't use the --schema or --catalog."""
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stderr', new=output):
            cmdline.main(['critique'])

    result = output.getvalue()
    expected = '--schema or --catalog must be specified'
    assert expected in result


def test_critique_cmdline_schema_in_catalog_files():
    """Critique cmdline should give a sys exit if schema file is in catalog."""
    schema_file = os.path.join(RESOURCE_PATH, 'alternative.yaml')
    output = io.StringIO()

    with pytest.raises(SystemExit):
        with mock.patch('sys.stderr', new=output):
            cmdline.main([
                'critique', '--schema', schema_file, '--catalog', schema_file
            ])

    result = output.getvalue()
    expected = 'is given for both --schema and --catalog'
    assert expected in result
