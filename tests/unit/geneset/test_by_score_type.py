"""Test the geneset get by score type."""

import pytest
from geneweaver.core.enum import ScoreType
from geneweaver.db.aio.geneset import get as async_get
from geneweaver.db.geneset import get


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
def test_by_score_type(score_type, example_genesets, cursor):
    """Test the geneset.get function by score type using a mock cursor."""
    cursor.fetchall.return_value = example_genesets
    result = get(cursor, score_type=score_type)
    assert result == example_genesets
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 0
    assert cursor.fetchall.call_count == 1


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
async def test_async_by_score_type(score_type, example_genesets, async_cursor):
    """Test the geneset.get function by score type using a mock asynch cursor."""
    async_cursor.fetchall.return_value = example_genesets
    result = await async_get(async_cursor, score_type=score_type)
    assert result == example_genesets
    assert async_cursor.execute.call_count == 1
    assert async_cursor.fetchone.call_count == 0
    assert async_cursor.fetchall.call_count == 1
