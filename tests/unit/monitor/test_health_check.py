"""Test DB health check function."""

from geneweaver.db.monitor.db_health import health_check

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


def test_health_check(cursor):
    """Test the db health check."""
    mock_return = {
        "gene_identifier_last_update": 1,
        "gene_count": 1,
        "geneset_count": 1,
    }
    cursor.fetchone.return_value = (1,)
    result = health_check(cursor)

    assert result == mock_return
    assert cursor.execute.call_count == 3
    assert cursor.fetchone.call_count == 3


test_get_execute_raises_error = create_execute_raises_error_test(health_check)

test_get_fetchone_raises_error = create_fetchone_raises_error_test(health_check)
