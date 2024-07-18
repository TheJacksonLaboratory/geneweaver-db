"""Test the ontology.get_ontology_dbs query generation function."""

import pytest
from geneweaver.db.query.ontology import get_ontology_dbs


@pytest.mark.parametrize("ontology_db_id", [None, 4])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
def test_all_kwargs(ontology_db_id, limit, offset):
    """Test all the kwarg combinations for query.ontology.get_ontology_dbs."""
    query, params = get_ontology_dbs(
        ontology_db_id=ontology_db_id,
        limit=limit,
        offset=offset,
    )

    str_query = str(query)

    for key in ["ontology_db_id", "name", "prefix", "url"]:
        assert key in str_query
