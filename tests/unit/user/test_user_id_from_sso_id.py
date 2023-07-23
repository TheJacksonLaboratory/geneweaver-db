"""Test for the user.user_id_from_sso_id function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.user import user_id_from_sso_id

from .const import MOCK_USER_DATA


@pytest.mark.parametrize(
    ("sso_id", "expected_result"),
    # The sso_id exists
    [(item["usr_sso_id"], item["usr_id"]) for item in MOCK_USER_DATA] +
    # The sso_id does not exist
    [("not a real SSO id", None)],
)
def test_by_api_key(sso_id, expected_result):
    """Test the user_id_from_sso_id function with a mock cursor."""
    cursor = Mock()
    # Fetchone should return a tuple
    cursor.fetchone.return_value = (expected_result,)
    result = user_id_from_sso_id(cursor, sso_id)
    # The function should unpack the tuple
    assert result == expected_result
    assert cursor.execute.call_count == 1
