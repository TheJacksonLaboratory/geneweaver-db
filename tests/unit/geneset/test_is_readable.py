"""Test the geneset.is_readable function."""
import pytest
from geneweaver.db.geneset import is_readable

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize("user_id", [1, 2, 3])
@pytest.mark.parametrize("geneset_id", [1, 2, 3])
@pytest.mark.parametrize("result", [[True], [False]])
def test_is_readable(user_id, geneset_id, result, cursor):
    """Test the geneset.is_readable function."""
    cursor.fetchone.return_value = result
    result = is_readable(cursor, user_id, geneset_id)
    assert result == result
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


test_is_readable_execute_raises_error = create_execute_raises_error_test(
    is_readable, 1, 1
)
test_is_readable_fetchone_raises_error = create_fetchone_raises_error_test(
    is_readable, 1, 1
)
