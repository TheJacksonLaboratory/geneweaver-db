"""Test for the user.by_sso_id function."""

from unittest.mock import Mock, patch

import pytest
from geneweaver.db.user import by_sso_id

from .const import MOCK_USER_DATA


@patch("geneweaver.db.user.User", dict)
@pytest.mark.parametrize(
    ("sso_id", "expected_result"),
    [(item["usr_sso_id"], item) for item in MOCK_USER_DATA],
)
def test_by_api_key(sso_id, expected_result):
    """Test the user by sso id function with a mock cursor."""
    cursor = Mock()
    cursor.fetchone.return_value = expected_result
    result = by_sso_id(cursor, sso_id)
    assert result == expected_result
    assert cursor.execute.call_count == 1


def test_by_sso_id_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_sso_id(cursor, "sso_id")

    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0


def test_by_sso_id_fetchone_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchone raises an error."""
    cursor = Mock()
    cursor.fetchone.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_sso_id(cursor, "sso_id")

    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
