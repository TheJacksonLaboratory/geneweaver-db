"""Test the general geneset.get function."""

import datetime

import pytest
from geneweaver.db.aio.geneset import get as async_get
from geneweaver.db.geneset import get

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_get_execute_raises_error = create_execute_raises_error_test(
    get,
)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(
    get,
)

test_async_get_execute_raises_error = async_create_execute_raises_error_test(
    async_get,
)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_get,
)


@pytest.mark.parametrize("created_after", [None, datetime.datetime(2008, 7, 31)])
@pytest.mark.parametrize("created_before", [None, datetime.datetime(2024, 7, 31)])
def test_get_gs_by_create_date(created_before, created_after, example_genesets, cursor):
    """Test the geneset.get function by create date using a mock cursor."""
    cursor.fetchall.return_value = example_genesets
    result = get(cursor, created_before=created_before, created_after=created_after)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("updated_after", [None, datetime.datetime(2008, 7, 31)])
@pytest.mark.parametrize("updated_before", [None, datetime.datetime(2024, 7, 31)])
def test_get_gs_by_update_date(updated_before, updated_after, example_genesets, cursor):
    """Test the geneset.get function by update date a mock cursor."""
    cursor.fetchall.return_value = example_genesets
    result = get(cursor, updated_before=updated_before, updated_after=updated_after)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("lte_count", [None, 20])
@pytest.mark.parametrize("gte_count", [None, 5])
def test_get_gs_gense_count_size(lte_count, gte_count, example_genesets, cursor):
    """Test the geneset.get function by update date a mock cursor."""
    cursor.fetchall.return_value = example_genesets
    result = get(cursor, lte_count=lte_count, gte_count=gte_count)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1
