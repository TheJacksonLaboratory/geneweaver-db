"""Test the PUB_QUERY generated constant."""

from psycopg.sql import SQL, Placeholder


def test_pub_insert_vals_types():
    """Test the PUB_INSERT_COLS generated constant."""
    from geneweaver.db.query.publication import PUB_INSERT_VALS

    for idx, value in enumerate(PUB_INSERT_VALS):
        if idx % 2 == 0:
            assert isinstance(value, Placeholder)
        else:
            assert isinstance(value, SQL)
            assert value == SQL(",")


def test_pub_id_not_in_pub_insert_vals():
    """Test that the pub_id is not in the PUB_INSERT_VALS constant."""
    from geneweaver.db.query.publication import PUB_INSERT_VALS

    for value in PUB_INSERT_VALS:
        assert "pub_id" not in str(value)
