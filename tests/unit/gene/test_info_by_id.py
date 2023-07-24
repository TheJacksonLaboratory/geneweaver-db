"""Test the gene.info_by_id function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.gene import info_by_gene_id

from .const import GENE_INFO


@pytest.mark.parametrize(
    ("gene_id", "expected"),
    [(item["ode_gene_id"], tuple(item.values())) for item in GENE_INFO],
)
def test_info_by_gene_id(gene_id, expected):
    """Test info_by_gene_id using a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = [expected]
    result = info_by_gene_id(cursor, gene_id)
    assert type(result) == list
    assert len(result) == 1
    assert result[0] == expected
    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1


def test_info_by_gene_id_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        info_by_gene_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 0


def test_info_by_gene_id_fetchall_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchall raises an error."""
    cursor = Mock()
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        info_by_gene_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
