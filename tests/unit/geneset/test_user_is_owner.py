"""Test the geneset.user_is_owner function."""
import pytest
from geneweaver.db.geneset import user_is_owner

from tests.unit.utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize(
    ("count_value", "expected_return"),
    [
        # If the count is 0, the user is not the owner.
        (0, False),
        # If the count is 1, the user is the owner.
        (1, True),
        # If the count is anything elsae, something is wrong,
        # but the user is NOT the owner.
        (2, False),
        (30, False),
        (5000, False),
        (-1, False),
        # The query should only return numbers, but should work for other
        # returns too
        (None, False),
        ("", False),
        ("a", False),
        ("b", False),
        (True, False),
        (False, False),
    ],
)
def test_user_is_owner_true(count_value, expected_return, cursor, example_user_id):
    """Test the user_is_owner function using a mock."""
    cursor.fetchone.return_value = (count_value,)
    result = user_is_owner(cursor, example_user_id, 1)
    assert result == expected_return
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


test_user_is_owner_execute_raises_error = create_execute_raises_error_test(
    user_is_owner, 1, 1
)

test_user_is_owner_fetchone_raises_error = create_fetchone_raises_error_test(
    user_is_owner, 1, 1
)
