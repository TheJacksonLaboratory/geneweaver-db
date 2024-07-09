"""Test the ontology.by_geneset query generation function."""

import pytest
from geneweaver.db.query.ontology import by_geneset


@pytest.mark.parametrize("geneset_id", [12345])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
def test_all_kwargs(geneset_id, limit, offset):
    """Test all the kwarg combinations for query.ontology.by_geneset."""
    query, params = by_geneset(
        geneset_id=geneset_id,
        limit=limit,
        offset=offset,
    )

    assert "gs_id" in params

    str_query = str(query)

    for key in ["ontology_term_id", "name", "description", "source_ontology"]:
        assert key in str_query
