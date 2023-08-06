import json

import pytest

from horkos.cmdline import check

CONTENT_TYPES = [
    'foo\nbar\nbaz',
    json.dumps([{'foo': 'bar'}, {'foo': 'baz'}]),
    json.dumps({'foo': 'bar'}) + '\n' + json.dumps({'foo': 'baz'}),
]


@pytest.mark.parametrize('content', CONTENT_TYPES)
def test_convert_to_records_csv(content):
    """Should be able to convert several file types to a list of records."""
    result = check._convert_to_records(content)

    assert result[0]['foo'] == 'bar'
    assert result[1]['foo'] == 'baz'
