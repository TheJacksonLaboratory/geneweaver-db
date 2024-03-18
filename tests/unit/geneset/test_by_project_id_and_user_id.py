"""Test the geneset.by_project_id_and_user_id function."""

from geneweaver.db.geneset import get

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


def test_by_project_id_and_user_id(
    example_genesets, example_primary_key, example_user_id, cursor
):
    """Test the geneset.by_project_id_and_user_id function using a mock cursor."""
    cursor.fetchall.return_value = example_genesets
    result = get(cursor, example_primary_key, example_user_id)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


test_by_project_id_and_user_id_execute_raises_error = create_execute_raises_error_test(
    get, 2, 1
)


test_by_project_id_and_user_id_fetchall_raises_error = (
    create_fetchall_raises_error_test(get, 2, 1)
)
