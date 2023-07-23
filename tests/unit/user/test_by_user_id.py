"""Test for the user.by_user_id function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.user import by_user_id

from .const import MOCK_USER_DATA


@pytest.mark.parametrize(
    ("user_id", "expected_result"),
    [(item["usr_id"], [item]) for item in MOCK_USER_DATA],
)
def test_by_api_key(user_id, expected_result):
    """Test the user by user id function with a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = expected_result
    result = by_user_id(cursor, user_id)
    assert result == expected_result
    assert cursor.execute.call_count == 1
