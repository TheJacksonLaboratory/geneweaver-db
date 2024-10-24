"""Test for the user.by_user_id function."""

from unittest.mock import Mock, patch

import pytest
from geneweaver.db.user import by_user_id

from .const import MOCK_USER_DATA


@patch("geneweaver.db.user.User", dict)
@pytest.mark.parametrize(
    ("user_id", "expected_result"),
    [(item["usr_id"], item) for item in MOCK_USER_DATA],
)
def test_by_api_key(user_id, expected_result):
    """Test the user by user id function with a mock cursor."""
    cursor = Mock()
    cursor.fetchone.return_value = expected_result
    result = by_user_id(cursor, user_id)
    assert result == expected_result
    assert cursor.execute.call_count == 1


def test_by_user_id_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_user_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0


def test_by_user_id_fetchone_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchone raises an error."""
    cursor = Mock()
    cursor.fetchone.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_user_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
