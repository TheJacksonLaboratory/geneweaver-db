"""Test the geneset.tier function."""
from geneweaver.db.geneset import tier

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


def test_tier(cursor, geneset_curation_id, example_primary_key):
    """Test the geneset.tier function."""
    cursor.fetchone.return_value = (
        geneset_curation_id if geneset_curation_id is None else (geneset_curation_id,)
    )
    assert tier(cursor, example_primary_key) == geneset_curation_id
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


test_tier_execute_raises_error = create_execute_raises_error_test(tier, 1)

test_tier_fetchone_raises_error = create_fetchone_raises_error_test(tier, 1)
