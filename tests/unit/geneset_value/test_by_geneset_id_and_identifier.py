"""Test the by_geneset_id_and_identifier function."""
from geneweaver.core.enum import GeneIdentifier
from geneweaver.db.geneset_value import by_geneset_id_and_identifier

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_by_geneset_id_and_identifier_execute_raises_error = (
    create_execute_raises_error_test(
        by_geneset_id_and_identifier, 1, GeneIdentifier.GENE_SYMBOL
    )
)
test_by_geneset_id_and_identifier_fetchall_raises_error = (
    create_fetchall_raises_error_test(
        by_geneset_id_and_identifier, 1, GeneIdentifier.GENE_SYMBOL
    )
)
