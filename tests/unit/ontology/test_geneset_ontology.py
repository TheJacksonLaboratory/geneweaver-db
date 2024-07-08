"""Test project ontology functions."""

import pytest
from geneweaver.db.aio.ontology import (
    add_ontology_to_geneset as async_add_ontology_to_geneset,
)
from geneweaver.db.ontology import add_ontology_to_geneset

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize("ont_id", [1])
@pytest.mark.parametrize("geneset_id", [1])
@pytest.mark.parametrize("gso_ref_type", ["test"])
def test_add_ontology_to_geneset(ont_id, geneset_id, gso_ref_type, cursor):
    """Test the ontology.add_ontology_to_geneset function."""
    cursor.fetchone.return_value = (1, 1)

    result = add_ontology_to_geneset(
        cursor=cursor,
        geneset_id=geneset_id,
        ontology_id=ont_id,
        gso_ref_type=gso_ref_type,
    )
    assert result == (1, 1)
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


@pytest.mark.parametrize("ont_id", [1])
@pytest.mark.parametrize("geneset_id", [1])
@pytest.mark.parametrize("gso_ref_type", ["test"])
async def test_async_add_ontology_to_geneset(
    ont_id, geneset_id, gso_ref_type, async_cursor
):
    """Test the ontology.add_ontology_to_geneset function."""
    async_cursor.fetchone.return_value = (1, 1)

    result = await async_add_ontology_to_geneset(
        cursor=async_cursor,
        geneset_id=geneset_id,
        ontology_id=ont_id,
        gso_ref_type=gso_ref_type,
    )
    assert result == (1, 1)
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 1
    assert async_cursor.fetchall.call_count == 0


test_add_execute_raises_error = create_execute_raises_error_test(
    add_ontology_to_geneset, 1, 1, "test"
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    add_ontology_to_geneset, 1, 1, "test"
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_add_ontology_to_geneset, 1, 1, "test"
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_add_ontology_to_geneset, 1, 1, "test"
)
