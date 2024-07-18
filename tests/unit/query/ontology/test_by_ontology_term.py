"""Test the ontology.by_ontology_term query generation function."""

import pytest
from geneweaver.db.query.ontology import by_ontology_term


@pytest.mark.parametrize("onto_ref_term_id", ["MA:0001955"])
def test_all_kwargs(onto_ref_term_id):
    """Test all the kwarg combinations for query.ontology.by_ontology_term."""
    query, params = by_ontology_term(onto_ref_term_id=onto_ref_term_id)

    assert "onto_ref_term_id" in params

    str_query = str(query)

    for key in [
        "onto_id",
        "onto_ref_term_id",
        "name",
        "description",
        "source_ontology",
    ]:
        assert key in str_query
