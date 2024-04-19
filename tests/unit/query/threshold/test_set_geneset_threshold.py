"""Test the threshold.set_geneset_threshold query generation function."""

import pytest
from geneweaver.core.enum import ScoreType
from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query.threshold import set_geneset_threshold


@pytest.mark.parametrize(
    "geneset_id", [1, 12, 234, 3587, 120946, 234598723, 23490876543405, 23409823498623]
)
@pytest.mark.parametrize(
    "score_type",
    [
        ScoreType.BINARY,
        ScoreType.CORRELATION,
        ScoreType.EFFECT,
        ScoreType.P_VALUE,
        ScoreType.Q_VALUE,
    ],
)
@pytest.mark.parametrize(
    "threshold",
    [
        {"threshold_low": 0.5, "threshold": 0.9},
        {"threshold_low": 0.01, "threshold": 0.999},
        {"threshold": 0.9},
        {"threshold": 0.2},
    ],
)
def test_set_geneset_threshold(geneset_id, score_type, threshold):
    """Test the set_geneset_threshold function for both async and sync."""
    geneset_score_type = GenesetScoreType(score_type=score_type, **threshold)
    sql, params = set_geneset_threshold(geneset_id, geneset_score_type)
    assert sql is not None
    assert params is not None

    if "threshold_low" in threshold:
        assert "threshold_low" in params
    else:
        assert "threshold_low" not in params

    assert "threshold" in params
    assert "geneset_id" in params
    assert "score_type" in params
