"""Test the restrict_tier function in the geneset query module."""

import pytest
from geneweaver.core.enum import GenesetTier
from psycopg.sql import SQL

from src.geneweaver.db.query.geneset.utils import restrict_tier


@pytest.mark.parametrize(
    "existing_filters",
    [
        [],
        [SQL("production.geneset_is_readable2(%(is_readable_by)s, geneset.gs_id)")],
        [
            SQL("production.geneset_is_readable2(%(is_readable_by)s, geneset.gs_id)"),
            SQL("geneset.gs_id = %(gs_id)s"),
        ],
        [
            SQL("production.geneset_is_readable2(%(is_readable_by)s, geneset.gs_id)"),
            SQL("geneset.gs_id = %(gs_id)s"),
            SQL("geneset.gs_owner = %(owner_id)s"),
        ],
    ],
)
@pytest.mark.parametrize(
    "existing_params",
    [
        {},
        {"is_readable_by": 1},
        {"is_readable_by": 1, "gs_id": 1},
        {"is_readable_by": 1, "gs_id": 1, "owner_id": 1},
    ],
)
@pytest.mark.parametrize(
    "curation_tier",
    [
        None,
        set(),
        GenesetTier.TIER1,
        GenesetTier.TIER2,
        GenesetTier.TIER3,
        GenesetTier.TIER4,
        GenesetTier.TIER5,
        {GenesetTier.TIER1},
        {GenesetTier.TIER1, GenesetTier.TIER2},
        {GenesetTier.TIER1, GenesetTier.TIER2, GenesetTier.TIER3},
        {GenesetTier.TIER1, GenesetTier.TIER2, GenesetTier.TIER3, GenesetTier.TIER4},
        {
            GenesetTier.TIER1,
            GenesetTier.TIER2,
            GenesetTier.TIER3,
            GenesetTier.TIER4,
            GenesetTier.TIER5,
        },
    ],
)
def test_restrict_tier(existing_filters, existing_params, curation_tier):
    """Test the restrict_tier function."""
    # Make a copy of the existing filters and params for use in this test only.
    these_existing_filters = existing_filters.copy()
    these_existing_params = existing_params.copy()

    filters, params = restrict_tier(
        these_existing_filters, these_existing_params, curation_tier
    )

    assert filters == these_existing_filters
    assert params == these_existing_params

    # If no curation tier is provided, the filters and params should be unchanged
    if curation_tier is None:
        assert filters == existing_filters
        assert params == existing_params

    else:
        # If a curation tier is provided, the filters should be updated
        assert len(filters) == len(existing_filters) + 1
        assert str(filters[-1]) == "SQL('geneset.cur_id = ANY(%(curation_tier)s)')"

        # The params should be updated with the curation tier
        assert "curation_tier" in params
        if isinstance(curation_tier, GenesetTier):
            assert params["curation_tier"] == [int(curation_tier)]
        else:
            assert params["curation_tier"] == [int(tier) for tier in curation_tier]
