"""Test the PUB_INSERT_COLS generated constant."""

from psycopg.sql import SQL, Identifier


def test_pub_insert_cols_types():
    """Test the PUB_INSERT_COLS generated constant."""
    from geneweaver.db.query.publication import PUB_INSERT_COLS

    for idx, value in enumerate(PUB_INSERT_COLS):
        assert "pub_id" not in str(value)
        if idx % 2 == 0:
            assert isinstance(value, Identifier)
        else:
            assert isinstance(value, SQL)
            assert value == SQL(",")


def test_pub_id_not_in_pub_insert_cols():
    """Test the PUB_INSERT_COLS generated constant."""
    from geneweaver.db.query.publication import PUB_INSERT_COLS

    for value in PUB_INSERT_COLS:
        assert "pub_id" not in str(value)
