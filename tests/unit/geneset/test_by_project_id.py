"""Test the geneset.by_project_id function."""

from geneweaver.db.geneset import by_project_id

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


def test_by_project_id(example_genesets, example_primary_key, cursor):
    """Test the geneset.by_project_id function."""
    cursor.fetchall.return_value = example_genesets
    result = by_project_id(cursor, example_primary_key)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


test_by_project_id_execute_raises_error = create_execute_raises_error_test(
    by_project_id, 1
)

test_by_project_id_fetchall_raises_error = create_fetchall_raises_error_test(
    by_project_id, 1
)
