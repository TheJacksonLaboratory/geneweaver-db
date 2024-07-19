"""Test the ontology.by_ontology_term db function."""

import pytest
from geneweaver.db.aio.ontology import (
    by_ontology_term as async_by_ontology_term,
)
from geneweaver.db.ontology import by_ontology_term

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize("onto_ref_term_id", ["MA:0001955"])
@pytest.mark.parametrize("ontologies_resp", ["a", "b", "c"])
def test_by_ontology_term(onto_ref_term_id, ontologies_resp, cursor):
    """Test the ontology.by_ontology_term function."""
    cursor.fetchone.return_value = ontologies_resp

    result = by_ontology_term(
        cursor=cursor,
        onto_ref_term_id=onto_ref_term_id,
    )
    assert result == ontologies_resp
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


@pytest.mark.parametrize("onto_ref_term_id", ["MA:0001955"])
@pytest.mark.parametrize("ontologies_resp", ["a", "b", "c"])
async def test_async_test_by_ontology_term(
    onto_ref_term_id,
    ontologies_resp,
    async_cursor,
):
    """Test the async ontology.by_ontology_term function."""
    async_cursor.fetchone.return_value = ontologies_resp

    result = await async_by_ontology_term(
        cursor=async_cursor,
        onto_ref_term_id=onto_ref_term_id,
    )
    assert result == ontologies_resp
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 1
    assert async_cursor.fetchall.call_count == 0


test_get_execute_raises_error = create_execute_raises_error_test(
    by_ontology_term, "term"
)

test_get_fetchone_raises_error = create_fetchone_raises_error_test(
    by_ontology_term, "term"
)

test_get_execute_raises_error = async_create_execute_raises_error_test(
    async_by_ontology_term, "term"
)

test_async_get_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_by_ontology_term, "term"
)
