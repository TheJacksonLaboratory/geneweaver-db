"""Test the threshold.set_geneset_threshold query generation function."""

import pytest
from geneweaver.core.enum import ScoreType
from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query.threshold import set_geneset_threshold


@pytest.mark.parametrize(
    "geneset_id",
    [0, 1, 12, 234, 3587, 120946, 234598723, 23490876543405, 23409823498623],
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
        {"threshold_low": 0.00001, "threshold": 0.899},
        {"threshold_low": 0.001, "threshold": 0.34599},
        {"threshold": 0.9},
        {"threshold": 0.2},
    ],
)
def test_set_geneset_threshold(geneset_id, score_type, threshold):
    """Test the set_geneset_threshold function for both async and sync."""
    geneset_score_type = GenesetScoreType(score_type=score_type, **threshold)
    sql, params = set_geneset_threshold(geneset_id, geneset_score_type)

    # Ensure that the SQL query and params are not None
    assert sql is not None
    assert params is not None

    str_sql = str(sql)

    # SQL query should contain the threshold, score_type, and geneset_id
    for query_item in [
        "%(threshold_str)s",
        "%(score_type)s",
        "%(geneset_id)s",
        " gs_id ",
        " gs_threshold_type ",
    ]:
        assert query_item in str_sql

    assert " id =" not in str_sql
    assert " threshold_type =" not in str_sql

    # Params should contain the threshold, score_type, and geneset_id
    for param_item in ["threshold_str", "score_type", "geneset_id"]:
        assert param_item in params

    assert params["score_type"] == int(score_type)
    assert params["geneset_id"] == geneset_id

    # SQL should always contain code to update gsv_in_threshold
    for case_item in ["gs_threshold_type", "gs_threshold", "UPDATE geneset"]:
        assert case_item in str_sql

    # If threshold_low is in the threshold, the SQL query should contain threshold_low
    if "threshold_low" in threshold:
        assert str(threshold["threshold_low"]) in params["threshold_str"]
        assert str(threshold["threshold"]) in params["threshold_str"]
        assert (
            params["threshold_str"]
            == f"{threshold['threshold_low']},{threshold['threshold']}"
        )
    else:
        assert params["threshold_str"] == str(threshold["threshold"])


@pytest.mark.parametrize(
    "geneset_id",
    [0, 1, 12, 234, 3587, 120946, 234598723, 23490876543405, 23409823498623],
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
        {"threshold_low": 0.5, "threshold": 0.3},
        {"threshold_low": 0.01, "threshold": 0.001},
        {"threshold_low": 0.9, "threshold": 0.899},
        {"threshold_low": 0.801, "threshold": 0.34599},
    ],
)
def test_set_geneset_threshold_error(geneset_id, score_type, threshold):
    """Test the set_geneset_threshold function for an error."""
    geneset_id = 0
    geneset_score_type = GenesetScoreType(
        score_type=score_type,
        threshold_low=threshold["threshold_low"],
        threshold=threshold["threshold"],
    )

    error_str = (
        "geneset_score_type.threshold must be larger "
        "than geneset_score_type.threshold_low"
    )

    with pytest.raises(ValueError, match=error_str):
        set_geneset_threshold(geneset_id, geneset_score_type)
