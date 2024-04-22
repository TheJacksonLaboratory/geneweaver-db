"""Test the set_geneset_threshold function for both async and sync."""

from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.aio.threshold import (
    set_geneset_threshold as async_set_geneset_threshold,
)
from geneweaver.db.threshold import set_geneset_threshold

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    create_execute_raises_error_test,
)

test_set_geneset_threshold_execute_raises_error = create_execute_raises_error_test(
    set_geneset_threshold, 1, GenesetScoreType(score_type="binary", threshold=0.05)
)

test_async_set_geneset_threshold_execute_raises_error = (
    async_create_execute_raises_error_test(
        async_set_geneset_threshold,
        1,
        GenesetScoreType(score_type="binary", threshold=0.05),
    )
)
