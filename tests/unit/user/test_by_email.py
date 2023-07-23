"""Test for the user.by_email function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.user import by_email

from .const import MOCK_USER_DATA


@pytest.mark.parametrize(
    ("email", "expected_result"),
    [(item["usr_email"], [item]) for item in MOCK_USER_DATA],
)
def test_by_api_key(email, expected_result):
    """Test the user by ap key function with a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = expected_result
    result = by_email(cursor, email)
    assert result == expected_result
    assert cursor.execute.call_count == 1
