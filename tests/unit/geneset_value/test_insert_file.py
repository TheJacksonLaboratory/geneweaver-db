"""Test the database interaction for inserting a geneset values file."""

import pytest
from geneweaver.db.exceptions import GeneweaverTypeError
from geneweaver.db.geneset_value import insert_file

from tests.unit.testing_utils import get_magic_mock_cursor


@pytest.mark.parametrize(
    ("formatted_file", "comments", "expected_result"),
    [
        ("some_file_string", "some_comments_string", 1),
        ("some_file_string", None, 2),
        ("some_file_string\nwith newlines\n", None, 3),
        ("some_file_string\nwith newlines\n", "some_comments_string", 4),
        (
            "some_file_string\nwith newlines\n",
            "some_comments_string\nwith newlines\n",
            5,
        ),
        ("some_file_string\nwith\ttabs\nand\tnewlines", None, 6),
        ("some_file_string\nwith\ttabs\nand\tnewlines", "some_comment", 6),
    ],
)
def test_insert_file(formatted_file, comments, expected_result):
    """Test the insert_file function happy path.

    Should call .execute, should return the file_id.
    """
    # Prepare the mock cursor
    cursor = get_magic_mock_cursor((expected_result,))

    if comments is not None:
        result = insert_file(cursor, formatted_file, comments)
    else:
        result = insert_file(cursor, formatted_file)

    assert result == expected_result
    assert cursor.execute.called is True
    assert "file" in cursor.execute.call_args[0][0]
    assert "RETURNING file_id" in cursor.execute.call_args[0][0]
    assert formatted_file in cursor.execute.call_args[0][1]
    if comments is not None:
        assert comments in cursor.execute.call_args[0][1]


@pytest.mark.parametrize(
    ("formatted_file", "comments"),
    [
        (None, "some_comments_string"),
        (None, None),
        (None, ""),
        ("", None),
        ("", ""),
        ("", "some_comments_string"),
    ],
)
def test_insert_file_error(formatted_file, comments):
    """The function should raise a GeneweaverTypeError for incorrect args."""
    cursor = get_magic_mock_cursor(None)

    if comments is not None:
        with pytest.raises(GeneweaverTypeError):
            _ = insert_file(cursor, formatted_file, comments)
    else:
        with pytest.raises(GeneweaverTypeError):
            _ = insert_file(cursor, formatted_file)
