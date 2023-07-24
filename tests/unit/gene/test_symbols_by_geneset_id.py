"""Test the gene.symbols_by_geneset_id function."""
from unittest.mock import Mock

import pytest
from geneweaver.db.gene import symbols_by_geneset_id


def test_symbols_by_geneset_id(geneset_gene_symbols):
    """Test symbols_by_geneset_id using a mock cursor."""
    cursor = Mock()
    cursor.fetchall.return_value = geneset_gene_symbols
    result = symbols_by_geneset_id(cursor, 1)
    assert type(result) == list
    assert len(result) == len(geneset_gene_symbols)
    assert result == geneset_gene_symbols
    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1


def test_gene_database_by_id_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        symbols_by_geneset_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 0


def test_gene_database_by_id_fetchall_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchall raises an error."""
    cursor = Mock()
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        symbols_by_geneset_id(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
