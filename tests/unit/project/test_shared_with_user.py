"""Test the project.shared_with_user db function."""

import pytest
from geneweaver.db.aio.project import shared_with_user as async_shared_with_user
from geneweaver.db.project import shared_with_user

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("user_id", [None, 47])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
@pytest.mark.parametrize(
    "projects",
    [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ],
)
def test_shared_with_user(user_id, limit, offset, projects, cursor):
    """Test the project.shared_with_user function."""
    cursor.fetchall.return_value = projects

    result = shared_with_user(
        cursor=cursor,
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
    assert result == projects
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("user_id", [None, 47])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
@pytest.mark.parametrize(
    "projects",
    [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ],
)
async def test_async_shared_with_user(user_id, limit, offset, projects, async_cursor):
    """Test the project.shared_with_user function."""
    async_cursor.fetchall.return_value = projects

    result = await async_shared_with_user(
        cursor=async_cursor,
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
    assert result == projects
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1


test_get_execute_raises_error = create_execute_raises_error_test(shared_with_user, 1)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(shared_with_user, 1)

test_get_execute_raises_error = async_create_execute_raises_error_test(
    async_shared_with_user, 1
)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_shared_with_user, 1
)
