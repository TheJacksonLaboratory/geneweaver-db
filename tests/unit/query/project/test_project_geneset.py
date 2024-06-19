"""Test project genset functions."""

from geneweaver.db.query.project import (
    insert_geneset_to_project,
    remove_geneset_from_project,
)
from psycopg.sql import SQL, Composed, Identifier, Placeholder


def test_insert_project_geneset():
    """Test the insert project geneset query generation function."""
    query, params = insert_geneset_to_project(
        project_id=1,
        geneset_id=1,
    )
    for item in query:
        assert any(
            isinstance(item, t) for t in [SQL, Composed, Identifier, Placeholder]
        )


def test_remove_project_geneset():
    """Test the remove project geneset query generation function."""
    query, params = remove_geneset_from_project(
        project_id=1,
        geneset_id=1,
    )
    for item in query:
        assert any(
            isinstance(item, t) for t in [SQL, Composed, Identifier, Placeholder]
        )
