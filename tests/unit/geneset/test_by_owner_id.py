"""Test the geneset.by_owner_id function."""

import pytest
from geneweaver.db.aio.geneset import by_owner_id as async_by_owner_id
from geneweaver.db.geneset import by_owner_id

from tests.unit.geneset.const import GENESETS
from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("user_id", [1, 101, 1001, 10001])
@pytest.mark.parametrize("geneset", GENESETS + [GENESETS[:3]] + [GENESETS])
def test_by_owner_id(geneset, user_id, cursor):
    """Test the geneset.by_owner_id function using a mock."""
    cursor.fetchall.return_value = [geneset]
    result = by_owner_id(cursor, user_id)
    assert result == [geneset]
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("user_id", [1, 101, 1001, 10001])
@pytest.mark.parametrize("geneset", GENESETS + [GENESETS[:3]] + [GENESETS])
async def async_test_by_owner_id(geneset, user_id, async_cursor):
    """Test the geneset.by_owner_id function using a mock."""
    async_cursor.fetchall.return_value = [geneset]
    result = await async_by_owner_id(async_cursor, user_id)
    assert result == [geneset]
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1


test_by_owner_id_execute_raises_error = create_execute_raises_error_test(by_owner_id, 1)

test_by_owner_id_fetchall_raises_error = create_fetchall_raises_error_test(
    by_owner_id, 1
)

test_async_by_owner_id_execute_raises_error = async_create_execute_raises_error_test(
    async_by_owner_id, 1
)

test_async_by_owner_id_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_by_owner_id, 1
)
