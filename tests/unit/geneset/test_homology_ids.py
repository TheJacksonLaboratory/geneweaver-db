"""Test the geneset.homology_ids function."""

import pytest
from geneweaver.db.geneset import homology_ids

from tests.unit.geneset.const import GENESET_HOM_IDS
from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)


@pytest.mark.parametrize(
    "hom_ids",
    [GENESET_HOM_IDS]
    + [GENESET_HOM_IDS[:5]]
    + [GENESET_HOM_IDS[5:]]
    + [GENESET_HOM_IDS[10:20]],
)
def test_homology_ids(hom_ids, example_primary_key, cursor):
    """Test the geneset.homology_ids function using a mock cursor."""
    cursor.fetchall.return_value = hom_ids
    result = homology_ids(cursor, example_primary_key)

    assert result == hom_ids
    assert cursor.execute.call_count == 1
    assert cursor.fetchall.call_count == 1
    assert "DISTINCT" in cursor.execute.call_args[0][0]
    assert example_primary_key in cursor.execute.call_args[0][1].values()


test_homology_ids_execute_raises_error = create_execute_raises_error_test(
    homology_ids, 1
)

test_homology_ids_fetchall_raises_error = create_fetchall_raises_error_test(
    homology_ids, 1
)
