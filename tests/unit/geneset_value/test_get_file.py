"""Test the geneset_values.get_file function."""
import pytest
from geneweaver.db.geneset_value import get_file

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize(
    "file_contents",
    [
        "some_file_contents",
        "some_file_contents\nwith newlines\n",
        "some_file_contents\nwith\ttabs\nand\tnewlines",
        "some_file_contents\nwith newlines\nand\ttabs",
        "some_file_contents\nwith\ttabs\nand newlines",
        None,
    ],
)
def test_get_file(example_primary_key, file_contents, cursor):
    """Test the get_file function happy path."""
    cursor.fetchone.return_value = (
        file_contents if file_contents is None else (file_contents,)
    )
    result = get_file(cursor, example_primary_key)

    expected = "" if file_contents is None else file_contents

    assert result == expected
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


test_get_file_execute_raises_error = create_execute_raises_error_test(get_file, 1)

test_get_file_fetchone_raises_error = create_fetchone_raises_error_test(get_file, 1)
