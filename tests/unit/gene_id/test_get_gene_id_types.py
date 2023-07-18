import pytest
from geneweaver.db.gene_id import get_gene_id_types
from tests.unit.gene_id.const import GENE_ID_TYPES
from tests.unit.db.utils import get_magic_mock_cursor

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


@pytest.mark.parametrize("species_id, expected_result", test_cases)
def test_get_gene_id_types(species_id, expected_result):
    """Test getting all the Gene ID types from the database."""
    cursor = get_magic_mock_cursor(expected_result)

    result = get_gene_id_types(cursor, species_id)

    assert result == expected_result

    assert 'ORDER BY gdb_id' in cursor.execute.call_args[0][0]

    if species_id is None:
        assert len(cursor.execute.call_args[0]) == 1
    else:
        assert len(cursor.execute.call_args[0]) == 2
        assert cursor.execute.call_args[0][1]['sp_id'] == species_id
