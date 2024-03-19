"""Test the get_gene_id_types function."""

from unittest.mock import Mock

import pytest
from geneweaver.db import gene

from tests.unit.gene.const import GENE_ID_TYPES
from tests.unit.testing_utils import get_magic_mock_cursor

test_cases = [
    (None, GENE_ID_TYPES),
    (0, list(filter(lambda row: row[2] == 0, GENE_ID_TYPES))),
    (1, list(filter(lambda row: row[2] == 0 or row[2] == 1, GENE_ID_TYPES))),
    (2, list(filter(lambda row: row[2] == 0 or row[2] == 2, GENE_ID_TYPES))),
    (3, list(filter(lambda row: row[2] == 0 or row[2] == 3, GENE_ID_TYPES))),
    (4, list(filter(lambda row: row[2] == 0 or row[2] == 4, GENE_ID_TYPES))),
    (5, list(filter(lambda row: row[2] == 0 or row[2] == 5, GENE_ID_TYPES))),
    (8, list(filter(lambda row: row[2] == 0 or row[2] == 8, GENE_ID_TYPES))),
    (9, list(filter(lambda row: row[2] == 0 or row[2] == 9, GENE_ID_TYPES))),
    (10, list(filter(lambda row: row[2] == 0 or row[2] == 10, GENE_ID_TYPES))),
]


@pytest.mark.parametrize(("species_id", "expected_result"), test_cases)
def test_get_gene_id_types(species_id, expected_result):
    """Test getting all the Gene ID types from the database."""
    cursor = get_magic_mock_cursor(expected_result)

    result = gene.id_types(cursor, species_id)

    assert result == expected_result

    assert "ORDER BY gdb_id" in cursor.execute.call_args[0][0]

    if species_id is None:
        assert len(cursor.execute.call_args[0]) == 1
    else:
        assert len(cursor.execute.call_args[0]) == 2
        assert cursor.execute.call_args[0][1]["sp_id"] == species_id


def test_gene_id_types_execute_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.execute raises an error."""
    cursor = Mock()
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        gene.id_types(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 0


def test_gene_id_types_fetchall_raises_error(all_psycopg_errors):
    """Test that the function raises an error when cursor.fetchall raises an error."""
    cursor = Mock()
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    with pytest.raises(all_psycopg_errors, match="Error message"):
        gene.id_types(cursor, 1)

    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
