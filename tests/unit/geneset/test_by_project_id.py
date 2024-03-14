"""Test the geneset.by_project_id function."""
import pytest
from geneweaver.db.aio.geneset import by_project_id as async_by_project_id
from geneweaver.db.geneset import by_project_id

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("is_readable_by", [None, 1, 102, 1003, 10005])
def test_by_project_id(is_readable_by, example_genesets, example_primary_key, cursor):
    """Test the geneset.by_project_id function."""
    cursor.fetchall.return_value = example_genesets
    result = by_project_id(cursor, example_primary_key, is_readable_by=is_readable_by)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("is_readable_by", [None, 1, 102, 1003, 10005])
async def test_async_by_project_id(
    is_readable_by, example_genesets, example_primary_key, async_cursor
):
    """Test the geneset.by_project_id function."""
    async_cursor.fetchall.return_value = example_genesets
    result = await async_by_project_id(
        async_cursor, example_primary_key, is_readable_by=is_readable_by
    )
    assert result == example_genesets
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1


test_by_project_id_execute_raises_error = create_execute_raises_error_test(
    by_project_id, 1
)

test_by_project_id_fetchall_raises_error = create_fetchall_raises_error_test(
    by_project_id, 1
)

test_async_by_project_id_execute_raises_error = async_create_execute_raises_error_test(
    async_by_project_id, 1
)

test_async_by_project_id_fetchall_raises_error = (
    async_create_fetchall_raises_error_test(async_by_project_id, 1)
)
