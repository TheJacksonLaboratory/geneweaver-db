"""Test the geneset.num_genes function."""

import pytest
from geneweaver.db.geneset import num_genes

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize("geneset_size", [0, 1, 2, 3, 4, 5])
def test_num_genes(example_primary_key, geneset_size, cursor):
    """Test that the num_genes function returns the expected number of genes."""
    cursor.fetchone.return_value = (geneset_size,)
    assert num_genes(cursor, example_primary_key) == geneset_size
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert "COUNT" in cursor.execute.call_args[0][0]
    assert example_primary_key in cursor.execute.call_args[0][1].values()


test_num_genes_execute_raises_error = create_execute_raises_error_test(num_genes, 1)

test_num_genes_fetchone_raises_error = create_fetchone_raises_error_test(num_genes, 1)
