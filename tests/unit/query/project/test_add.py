"""Test the project.add query generation function."""

from geneweaver.db.query.project import add
from psycopg.sql import SQL, Composed, Identifier, Placeholder


def test_project_add():
    """Test the add geneset query generation function."""
    query, params = add(
        user_id=1,
        name="a string",
        notes="a string",
        starred=False,
    )
    for item in query:
        assert any(
            isinstance(item, t) for t in [SQL, Composed, Identifier, Placeholder]
        )
