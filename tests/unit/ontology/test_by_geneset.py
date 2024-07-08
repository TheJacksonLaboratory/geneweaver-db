"""Test the ontology.by_geneset db function."""

import pytest
from geneweaver.db.aio.ontology import (
    by_geneset as async_get_ontology_by_gs_id,
)
from geneweaver.db.ontology import by_geneset

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("geneset_id", [12345])
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
def test_get_ontology_by_gs_id(geneset_id, limit, offset, ontologies_resp, cursor):
    """Test the ontology.get_ontology_by_gs_id function."""
    cursor.fetchall.return_value = ontologies_resp

    result = by_geneset(
        cursor=cursor,
        geneset_id=geneset_id,
        limit=limit,
        offset=offset,
    )
    assert result == ontologies_resp
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


@pytest.mark.parametrize("geneset_id", [12345])
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
async def test_async_get_ontology_by_gs_id(
    geneset_id,
    limit,
    offset,
    ontologies_resp,
    async_cursor,
):
    """Test the async ontology.get_ontology_by_gs_id function."""
    async_cursor.fetchall.return_value = ontologies_resp

    result = await async_get_ontology_by_gs_id(
        cursor=async_cursor,
        geneset_id=geneset_id,
        limit=limit,
        offset=offset,
    )
    assert result == ontologies_resp
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1


test_get_execute_raises_error = create_execute_raises_error_test(by_geneset, 1)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(by_geneset, 1)

test_get_execute_raises_error = async_create_execute_raises_error_test(
    async_get_ontology_by_gs_id, 1
)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_get_ontology_by_gs_id, 1
)
