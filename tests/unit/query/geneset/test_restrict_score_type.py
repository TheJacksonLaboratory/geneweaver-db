"""Test restrict_score_type function."""

import pytest
from geneweaver.core.enum import ScoreType
from psycopg.sql import SQL

from src.geneweaver.db.query.geneset.utils import restrict_score_type


@pytest.mark.parametrize("existing_filters", [[], [SQL("geneset.gs_id = %(gs_id)s")]])
@pytest.mark.parametrize("existing_params", [{}, {"gs_id": 1}])
@pytest.mark.parametrize(
    "score_type",
    [
        None,
        set(),
        ScoreType.P_VALUE,
        ScoreType.Q_VALUE,
        ScoreType.EFFECT,
        ScoreType.CORRELATION,
        ScoreType.BINARY,
        {ScoreType.P_VALUE},
        {ScoreType.P_VALUE, ScoreType.Q_VALUE},
        {ScoreType.P_VALUE, ScoreType.Q_VALUE, ScoreType.EFFECT},
        {ScoreType.P_VALUE, ScoreType.Q_VALUE, ScoreType.EFFECT, ScoreType.CORRELATION},
        {
            ScoreType.P_VALUE,
            ScoreType.Q_VALUE,
            ScoreType.EFFECT,
            ScoreType.CORRELATION,
            ScoreType.BINARY,
        },
    ],
)
def test_restrict_score_type(existing_filters, existing_params, score_type):
    """Test the restrict_score_type function."""
    # Make a copy of the existing filters and params for use in this test only.
    these_existing_filters = existing_filters.copy()
    these_existing_params = existing_params.copy()

    # Call the restrict_score_type function.
    new_filters, new_params = restrict_score_type(
        existing_filters=these_existing_filters,
        existing_params=these_existing_params,
        score_type=score_type,
    )

    # Check that the existing filters and params were not modified.
    if score_type is None:
        assert existing_filters == these_existing_filters
        assert existing_params == these_existing_params

    # Check that the new filters and params are correct.
    if score_type is not None:
        if isinstance(score_type, ScoreType):
            score_type = {score_type}

        assert new_filters == existing_filters + [
            SQL("geneset.gs_threshold_type = ANY(%(score_type)s)")
        ]
        assert new_params == {
            **existing_params,
            "score_type": [int(t) for t in score_type],
        }
    else:
        assert new_filters == existing_filters
        assert new_params == existing_params
