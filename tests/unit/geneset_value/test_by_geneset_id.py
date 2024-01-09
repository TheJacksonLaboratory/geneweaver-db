"""Test the geneset_values.by_genest_id function."""
import pytest
from unittest.mock import patch
from geneweaver.core.enum import GeneIdentifier
from geneweaver.db.geneset_value import by_geneset_id

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
    result = by_geneset_id(cursor, geneset_id)
    assert result == geneset_value
    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1


@patch("geneweaver.db.geneset_value.by_geneset_id_and_identifier")
@patch("geneweaver.db.geneset_value.by_geneset_id_as_uploaded")
def test_by_geneset_id_calls_correct_function(mock_as_uploaded, mock_identifier, cursor):
    """Test that the by_geneset_id function calls the correct function.

    It should call the by_geneset_id_and_identifier function if an identifier is
    provided, otherwise it should call the by_geneset_id_as_uploaded function.
    """
    _ = by_geneset_id(cursor, 1)
    assert mock_as_uploaded.call_count == 1
    assert mock_identifier.call_count == 0

    _ = by_geneset_id(cursor, 1, identifier=GeneIdentifier.ENSEMBLE_GENE)
    assert mock_as_uploaded.call_count == 1
    assert mock_identifier.call_count == 1


test_by_geneset_id_execute_raises_error = create_execute_raises_error_test(
    by_geneset_id, 1
)
test_by_geneset_id_fetchall_raises_error = create_fetchall_raises_error_test(
    by_geneset_id, 1
)

test_by_geneset_id_w_identifier_execute_raises_error = create_execute_raises_error_test(
    by_geneset_id, 1, identifier=GeneIdentifier.ENSEMBLE_GENE
)
test_by_geneset_id_w_identifier_fetchall_raises_error = create_fetchall_raises_error_test(
    by_geneset_id, 1, identifier=GeneIdentifier.ENSEMBLE_GENE
)
