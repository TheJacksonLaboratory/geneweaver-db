"""Test project geneset functions."""

import pytest
from geneweaver.db.aio.project import (
    add_geneset_to_project as async_add_geneset_to_project,
)
from geneweaver.db.aio.project import (
    delete_geneset_from_project as async_delete_geneset_to_project,
)
from geneweaver.db.project import add_geneset_to_project, delete_geneset_from_project

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize("project_id", [1])
@pytest.mark.parametrize("geneset_id", [1])
def test_add_geneset_to_project(project_id, geneset_id, cursor):
    """Test the project.add_geneset_to_project function."""
    cursor.fetchone.return_value = (1, 1)

    result = add_geneset_to_project(
        cursor=cursor, project_id=project_id, geneset_id=geneset_id
    )
    assert result == (1, 1)
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


@pytest.mark.parametrize("project_id", [1])
@pytest.mark.parametrize("geneset_id", [1])
def test_delete_geneset_from_project(project_id, geneset_id, cursor):
    """Test the project.delete_geneset_from_project function."""
    cursor.fetchone.return_value = (1, 1)

    result = delete_geneset_from_project(
        cursor=cursor, project_id=project_id, geneset_id=geneset_id
    )
    assert result == (1, 1)
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


@pytest.mark.parametrize("project_id", [1])
@pytest.mark.parametrize("geneset_id", [1])
async def test_async_add_geneset_to_project(project_id, geneset_id, async_cursor):
    """Test the project.add_geneset_to_project function."""
    async_cursor.fetchone.return_value = (1, 1)

    result = await async_add_geneset_to_project(
        cursor=async_cursor, project_id=project_id, geneset_id=geneset_id
    )
    assert result == (1, 1)
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 1
    assert async_cursor.fetchall.call_count == 0


@pytest.mark.parametrize("project_id", [1])
@pytest.mark.parametrize("geneset_id", [1])
async def test_async_delete_geneset_from_project(project_id, geneset_id, async_cursor):
    """Test the project.delete_geneset_from_project function."""
    async_cursor.fetchone.return_value = (1, 1)

    result = await async_delete_geneset_to_project(
        cursor=async_cursor, project_id=project_id, geneset_id=geneset_id
    )
    assert result == (1, 1)
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 1
    assert async_cursor.fetchall.call_count == 0


test_add_execute_raises_error = create_execute_raises_error_test(
    add_geneset_to_project, 1, 1
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    add_geneset_to_project, 1, 1
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_add_geneset_to_project, 1, 1
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_add_geneset_to_project, 1, 1
)

test_add_execute_raises_error = create_execute_raises_error_test(
    delete_geneset_from_project, 1, 1
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    delete_geneset_from_project, 1, 1
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_delete_geneset_to_project, 1, 1
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_delete_geneset_to_project, 1, 1
)
