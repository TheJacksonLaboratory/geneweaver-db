"""Full general search of Geneweaver Database."""

from datetime import date
from typing import Optional, Tuple

from geneweaver.db.query.geneset.utils import (
    format_select_query,
    is_readable,
    restrict_score_type,
    restrict_species,
    restrict_tier,
)
from geneweaver.db.query.search import const
from geneweaver.db.query.search.utils import search
from geneweaver.db.query.utils import add_op_filters, construct_filters
from geneweaver.db.utils import (
    GenesetScoreTypeOrScoreTypes,
    GenesetTierOrTiers,
    SpeciesOrSpeciesSet,
    limit_and_offset,
)
from psycopg.sql import SQL, Composed


def genesets(
    search_text: str,
    is_readable_by: Optional[int] = None,
    publication_id: Optional[int] = None,
    pubmed_id: Optional[int] = None,
    species: Optional[SpeciesOrSpeciesSet] = None,
    curation_tier: Optional[GenesetTierOrTiers] = None,
    score_type: Optional[GenesetScoreTypeOrScoreTypes] = None,
    lte_count: Optional[int] = None,
    gte_count: Optional[int] = None,
    created_before: Optional[date] = None,
    created_after: Optional[date] = None,
    updated_before: Optional[date] = None,
    updated_after: Optional[date] = None,
    limit: Optional[int] = 25,
    offset: Optional[int] = 0,
    _status: Optional[str] = "normal",
) -> Tuple[Composed, dict]:
    """Search genesets using all relevant metadata fields.

    :param search_text: Return genesets that match this search text.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param publication_id: Show only results with this publication ID (internal).
    :param pubmed_id: Show only results with this PubMed ID.
    :param species: Show only results associated with this species.
    :param curation_tier: Show only results of this curation tier.
    :param score_type: Show only results with given score type.
    :param lte_count: less than or equal count.
    :param gte_count: greater than or equal count.
    :param created_before: Show only results created before this date.
    :param created_after: Show only results updated before this date.
    :param updated_before: Show only results updated before this date.
    :param updated_after: Show only results updated after this date.
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :param _status: Show only results with this status. Default is "normal".
    """
    params = {}
    filtering = []

    query = format_select_query() + SQL(
        "JOIN geneset_search ON geneset_search.gs_id = geneset.gs_id"
    )

    filtering, params = is_readable(filtering, params, is_readable_by)
    filtering, params = search(
        filtering, params, const.SEARCH_COMBINED_COL, search_text
    )
    filtering, params = restrict_tier(filtering, params, curation_tier)
    filtering, params = restrict_score_type(filtering, params, score_type)
    filtering, params = restrict_species(filtering, params, species)

    filtering, params = add_op_filters(
        filtering,
        params,
        lte_count=lte_count,
        gte_count=gte_count,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        table="geneset",
    )

    filtering, params = construct_filters(
        filtering,
        params,
        {
            "gs_status": _status,
        },
        table="geneset",
    )

    filtering, params = construct_filters(
        filtering,
        params,
        {
            "pub_id": publication_id,
            "pub_pubmed": str(pubmed_id) if pubmed_id is not None else None,
        },
        table="geneset_search",
    )

    if len(filtering) > 0:
        query += SQL("WHERE") + SQL("AND").join(filtering)

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params
