"""Test the general geneset.get function."""

from geneweaver.db.aio.publication import get as async_get
from geneweaver.db.publication import get

from tests.unit.publication.const import (
    PUBMED_PUBLICATIONS,
)
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


def test_get_by(cursor):
    """Test the publication.get function by various parameters."""
    cursor.fetchall.return_value = PUBMED_PUBLICATIONS
    result = get(
        cursor=cursor,
        pub_id=1,
        authors="Author1, Author2",
        title="Title1",
        abstract="Abstract1",
        journal="Journal1",
        volume="Volume1",
        pages="Pages1",
        month="Month1",
        year="Year1",
        pubmed="123456",
        search_text="something",
    )
    assert result == PUBMED_PUBLICATIONS
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


async def test_async_get_by(async_cursor):
    """Test the async publication.get function by various parameters."""
    async_cursor.fetchall.return_value = PUBMED_PUBLICATIONS
    result = await async_get(
        cursor=async_cursor,
        pub_id=1,
        authors="Author1, Author2",
        title="Title1",
        abstract="Abstract1",
        journal="Journal1",
        volume="Volume1",
        pages="Pages1",
        month="Month1",
        year="Year1",
        pubmed="123456",
        search_text="something",
    )
    assert result == PUBMED_PUBLICATIONS
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1
