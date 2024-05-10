"""Test the geneset get with ontology term filter."""

from geneweaver.db.aio.geneset import get as async_get
from geneweaver.db.geneset import get


def test_by_ontology_term(example_genesets, cursor):
    """Test the geneset.get function by ontology term using a mock cursor."""
    cursor.fetchall.return_value = example_genesets
    result = get(cursor, ontology_term="D001522")
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


async def test_async_test_by_ontology_term(example_genesets, async_cursor):
    """Test the geneset.get function by ontology term using a mock asynch cursor."""
    async_cursor.fetchall.return_value = example_genesets
    result = await async_get(async_cursor, ontology_term="D001522")
    assert result == example_genesets
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1
