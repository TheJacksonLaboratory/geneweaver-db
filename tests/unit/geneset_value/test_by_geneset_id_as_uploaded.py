"""Test the geneset_values.by_genest_id function."""
import pytest
from geneweaver.db.geneset_value import by_geneset_id_as_uploaded

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize("geneset_id", [406756, 105683, 56893])
@pytest.mark.parametrize(
    "geneset_value",
    [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ],
)
def test_by_geneset_id(geneset_id, geneset_value, cursor):
    """Test the geneset_values.by_geneset_id function."""
    cursor.fetchall.return_value = geneset_value
    result = by_geneset_id_as_uploaded(cursor, geneset_id)
    assert result == geneset_value
    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1


test_by_geneset_id_as_uploaded_execute_raises_error = create_execute_raises_error_test(
    by_geneset_id_as_uploaded, 1
)
test_by_geneset_id_as_uploaded_fetchall_raises_error = (
    create_fetchall_raises_error_test(by_geneset_id_as_uploaded, 1)
)
