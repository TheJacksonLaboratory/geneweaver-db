"""Test the get_database_id function."""

from geneweaver.core.enum import GeneIdentifier
from geneweaver.db.gene import gene_database_id

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_gene_database_id_execute_raises_error = create_execute_raises_error_test(
    gene_database_id, identifier=GeneIdentifier.ENSEMBLE_GENE
)
test_gene_database_id_fetchall_raises_error = create_fetchall_raises_error_test(
    gene_database_id, identifier=GeneIdentifier.ENSEMBLE_GENE
)
