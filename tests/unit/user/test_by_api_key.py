"""Test for the user.by_api_key function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.user import by_api_key

from .const import MOCK_USER_DATA


@pytest.mark.parametrize(
    ("api_key", "expected_result"),
    [(item["apikey"], [item]) for item in MOCK_USER_DATA],
)
def test_by_api_key(api_key, expected_result):
    """Test the user by api key function with a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = expected_result
    result = by_api_key(cursor, api_key)
    assert result == expected_result
    assert cursor.execute.call_count == 1
