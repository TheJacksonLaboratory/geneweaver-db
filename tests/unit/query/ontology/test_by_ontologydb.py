"""Test the ontology.by_ontology_db query generation function."""

import pytest
from geneweaver.db.query.ontology import by_ontology_db


@pytest.mark.parametrize("ontology_db_id", [None, 4])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
def test_all_kwargs(ontology_db_id, limit, offset):
    """Test all the kwarg combinations for query.ontology.by_ontology_db."""
    query, params = by_ontology_db(
        ontology_db_id=ontology_db_id,
        limit=limit,
        offset=offset,
    )

    assert "ontology_db_id" in params

    str_query = str(query)

    for key in ["ontology_term_id", "name", "description", "source_ontology"]:
        assert key in str_query
