"""Test the project.get db function."""

import pytest
from geneweaver.db.aio.project import get as async_get
from geneweaver.db.project import get

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("project_id", [None, 12345])
@pytest.mark.parametrize("owner_id", [None, 47])
@pytest.mark.parametrize("name", [None, "test"])
@pytest.mark.parametrize("starred", [None, True, False])
@pytest.mark.parametrize("search_text", [None, "search text test"])
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
def test_get(
    project_id, owner_id, name, starred, search_text, limit, offset, projects, cursor
):
    """Test the project.get function."""
    cursor.fetchall.return_value = projects

    result = get(
        cursor=cursor,
        project_id=project_id,
        owner_id=owner_id,
        name=name,
        starred=starred,
        search_text=search_text,
        limit=limit,
        offset=offset,
    )
    assert result == projects
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("project_id", [None, 12345])
@pytest.mark.parametrize("owner_id", [None, 47])
@pytest.mark.parametrize("name", [None, "test"])
@pytest.mark.parametrize("starred", [None, True, False])
@pytest.mark.parametrize("search_text", [None, "search text test"])
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
async def test_async_get(
    project_id,
    owner_id,
    name,
    starred,
    search_text,
    limit,
    offset,
    projects,
    async_cursor,
):
    """Test the project.get function."""
    async_cursor.fetchall.return_value = projects

    result = await get(
        cursor=async_cursor,
        project_id=project_id,
        owner_id=owner_id,
        name=name,
        starred=starred,
        search_text=search_text,
        limit=limit,
        offset=offset,
    )
    assert result == projects
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1


test_get_execute_raises_error = create_execute_raises_error_test(get, 1)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(get, 1)

test_get_execute_raises_error = async_create_execute_raises_error_test(async_get, 1)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_get, 1
)
