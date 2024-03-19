"""Test for the user.by_email function."""

from unittest.mock import Mock

import pytest
from geneweaver.db.user import by_email

from .const import MOCK_USER_DATA


@pytest.mark.parametrize(
    ("email", "expected_result"),
    [(item["usr_email"], [item]) for item in MOCK_USER_DATA],
)
def test_by_email(email, expected_result):
    """Test the user by ap key function with a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = expected_result
    result = by_email(cursor, email)
    assert result == expected_result
    assert cursor.execute.call_count == 1


def test_by_email_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_email(cursor, "john.doe@jax.org")

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 0


def test_by_email_fetchall_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchall raises an error."""
    cursor = Mock()
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_email(cursor, "john.doe@jax.org")

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
