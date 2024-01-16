"""Test for the user.by_sso_id function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.user import by_sso_id_and_email

from .const import MOCK_USER_DATA


@pytest.mark.parametrize("email", ["email@email.com", "email@jax.org", "e.mail@jax.org"])
@pytest.mark.parametrize(
    ("sso_id", "expected_result"),
    [(item["usr_sso_id"], [item]) for item in MOCK_USER_DATA],
)
def test_by_api_key(sso_id, expected_result, email):
    """Test the user by sso id function with a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = expected_result
    result = by_sso_id_and_email(cursor, sso_id, email)
    assert result == expected_result
    assert cursor.execute.call_count == 1


def test_by_sso_id_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_sso_id_and_email(cursor, "sso_id", "email@email.com")

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 0


def test_by_sso_id_fetchall_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchall raises an error."""
    cursor = Mock()
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        by_sso_id_and_email(cursor, "sso_id", "email@email.com")

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
