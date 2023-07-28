"""Test the geneset.by_user_id function."""
import pytest
from geneweaver.db.geneset import by_user_id

from tests.unit.geneset.const import GENESETS
from tests.unit.utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("user_id", [1, 101, 1001, 10001])
@pytest.mark.parametrize("geneset", GENESETS + [GENESETS[:3]] + [GENESETS])
def test_by_user_id(geneset, user_id, cursor):
    """Test the geneset.by_user_id function using a mock."""
    cursor.fetchall.return_value = [geneset]
    result = by_user_id(cursor, user_id)
    assert result == [geneset]
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


test_by_user_id_execute_raises_error = create_execute_raises_error_test(by_user_id, 1)

test_by_user_id_fetchall_raises_error = create_fetchall_raises_error_test(by_user_id, 1)
