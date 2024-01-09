"""Test the get_homolog_ids_with_source_identifier."""
from geneweaver.core.enum import GeneIdentifier
from geneweaver.db.gene import get_homolog_ids_with_source_identifier

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_get_homolog_ids_with_source_identifier_execute_raises_error = (
    create_execute_raises_error_test(
        get_homolog_ids_with_source_identifier,
        ("1", "2"),
        source_identifier=GeneIdentifier.GENE_SYMBOL,
        result_identifier=GeneIdentifier.ENSEMBLE_GENE,
    )
)
test_get_homolog_ids_with_source_identifier_fetchall_raises_error = (
    create_fetchall_raises_error_test(
        get_homolog_ids_with_source_identifier,
        ("1", "2"),
        source_identifier=GeneIdentifier.GENE_SYMBOL,
        result_identifier=GeneIdentifier.ENSEMBLE_GENE,
    )
)
