"""Test for the user.by_api_key function."""

from unittest.mock import Mock, patch

import pytest
from geneweaver.db.user import by_api_key

from .const import MOCK_USER_DATA


@patch("geneweaver.db.user.User", dict)
@pytest.mark.parametrize(
    ("api_key", "expected_result"),
    [(item["apikey"], item) for item in MOCK_USER_DATA],
)
def test_by_api_key(api_key, expected_result):
    """Test the user by api key function with a mock cursor."""
    cursor = Mock()
    cursor.fetchone.return_value = expected_result
    result = by_api_key(cursor, api_key)
    assert result == expected_result
    assert cursor.execute.call_count == 1


def test_by_api_key_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_api_key(cursor, "1")

    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0


def test_by_api_key_fetchone_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchone raises an error."""
    cursor = Mock()
    cursor.fetchone.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_api_key(cursor, "1")

    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
