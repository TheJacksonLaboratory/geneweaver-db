"""Test the publication.by_id function."""
from geneweaver.db.publication import by_id

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

test_by_id_execute_raises_error = create_execute_raises_error_test(by_id, 1)

test_by_id_fetchone_raises_error = create_fetchone_raises_error_test(by_id, 1)


def test_get_publication_by_id(cursor):
    """Test getting a publication by id."""
    # Prepare the mock cursor
    cursor.fetchone.return_value = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    result = by_id(cursor, 12345)

    assert result == (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    assert 12345 in cursor.execute.call_args[0][1].values()
    assert cursor.fetchone.call_count == 1
