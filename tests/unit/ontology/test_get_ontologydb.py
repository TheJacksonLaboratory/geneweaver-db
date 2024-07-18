"""Test the ontology.get_ontology_dbs db function."""

import pytest
from geneweaver.db.aio.ontology import (
    get_ontology_dbs as async_get_ontology_dbs,
)
from geneweaver.db.ontology import get_ontology_dbs

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("ontology_db_id", [None, 4])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
@pytest.mark.parametrize(
    "ontologies_resp",
    [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ],
)
def test_get_ontology_dbs(ontology_db_id, limit, offset, ontologies_resp, cursor):
    """Test the ontology.get_ontology_dbs function."""
    cursor.fetchall.return_value = ontologies_resp

    result = get_ontology_dbs(
        cursor=cursor,
        ontology_db_id=ontology_db_id,
        limit=limit,
        offset=offset,
    )
    assert result == ontologies_resp
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("ontology_db_id", [None, 4])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
@pytest.mark.parametrize(
    "ontologies_resp",
    [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ],
)
async def test_async_get_ontology_dbs(
    ontology_db_id,
    limit,
    offset,
    ontologies_resp,
    async_cursor,
):
    """Test the async ontology.by_ontology_db function."""
    async_cursor.fetchall.return_value = ontologies_resp

    result = await async_get_ontology_dbs(
        cursor=async_cursor,
        ontology_db_id=ontology_db_id,
        limit=limit,
        offset=offset,
    )
    assert result == ontologies_resp
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1


test_get_execute_raises_error = create_execute_raises_error_test(get_ontology_dbs, 1)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(get_ontology_dbs, 1)

test_get_execute_raises_error = async_create_execute_raises_error_test(
    async_get_ontology_dbs, 1
)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_get_ontology_dbs, 1
)
