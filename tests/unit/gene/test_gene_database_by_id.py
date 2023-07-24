"""Test the gene.gene_database_by_id function."""
import pytest
from unittest.mock import Mock
from tests.unit.gene.const import GENE_ID_TYPES

from geneweaver.db.gene import gene_database_by_id


@pytest.mark.parametrize(
    ("gene_id", "expected_result"),
    [(item[0], item) for item in GENE_ID_TYPES])
def test_gene_database_by_id(gene_id, expected_result):
    """Test the gene_database_by_id function using a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = [expected_result]
    result = gene_database_by_id(cursor, gene_id)
    assert type(result) == list
    assert result[0] == expected_result
    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
    assert "genedb" in cursor.execute.call_args[0][0]


def test_gene_database_by_id_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        gene_database_by_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 0


def test_gene_database_by_id_fetchall_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchall raises an error."""
    cursor = Mock()
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        gene_database_by_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
