"""Test the get_homolog_ids_by_ode_id function."""

from geneweaver.core.enum import GeneIdentifier
from geneweaver.db.gene import get_homolog_ids_by_ode_id

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_get_homolog_ids_by_ode_id_execute_raises_error = create_execute_raises_error_test(
    get_homolog_ids_by_ode_id, ("1", "2"), identifier=GeneIdentifier.ENSEMBLE_GENE
)
test_get_homolog_ids_by_ode_id_fetchall_raises_error = (
    create_fetchall_raises_error_test(
        get_homolog_ids_by_ode_id, ("1", "2"), identifier=GeneIdentifier.ENSEMBLE_GENE
    )
)
