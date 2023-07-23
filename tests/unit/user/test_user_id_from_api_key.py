"""Test for the user.user_id_from_api_key function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.user import user_id_from_api_key

from .const import MOCK_USER_DATA


@pytest.mark.parametrize(
    ("apikey", "expected_result"),
    # The apikey exists
    [(item["apikey"], item["usr_id"]) for item in MOCK_USER_DATA] +
    # The apikey does not exist
    [("not a real api key", None)],
)
def test_by_api_key(apikey, expected_result):
    """Test the user_id_from_api_key function with a mock cursor."""
    cursor = Mock()
    # Fetchone should return a tuple
    cursor.fetchone.return_value = (expected_result,)
    result = user_id_from_api_key(cursor, apikey)
    # The function should unpack the tuple
    assert result == expected_result
    assert cursor.execute.call_count == 1
