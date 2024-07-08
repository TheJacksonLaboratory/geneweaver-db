"""Test geneset ontology functions."""

from geneweaver.db.query.ontology import (
    insert_geneset_ontology_term_association,
)
from psycopg.sql import SQL, Composed, Identifier, Placeholder


def test_insert_geneset_ontology():
    """Test the insert project geneset query generation function."""
    query, params = insert_geneset_ontology_term_association(
        geneset_id=1, ontology_term_id=1, gso_ref_type="test"
    )
    for item in query:
        assert any(
            isinstance(item, t) for t in [SQL, Composed, Identifier, Placeholder]
        )
