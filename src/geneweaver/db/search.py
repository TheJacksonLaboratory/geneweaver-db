"""Search genesets using all relevant metadata fields."""

from datetime import date
from typing import List, Optional

from geneweaver.db.query import search
from geneweaver.db.utils import (
    GenesetScoreTypeOrScoreTypes,
    GenesetTierOrTiers,
    SpeciesOrSpeciesSet,
)
from psycopg import Cursor
from psycopg.rows import Row


def genesets(
    cursor: Cursor,
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
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    _status: Optional[str] = "normal",
) -> List[Row]:
    """Search genesets using all relevant metadata fields.

    :param cursor: A database cursor.
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
    cursor.execute(
        *search.genesets(
            search_text,
            is_readable_by=is_readable_by,
            publication_id=publication_id,
            pubmed_id=pubmed_id,
            species=species,
            curation_tier=curation_tier,
            score_type=score_type,
            lte_count=lte_count,
            gte_count=gte_count,
            created_before=created_before,
            created_after=created_after,
            updated_before=updated_before,
            updated_after=updated_after,
            limit=limit,
            offset=offset,
            _status=_status,
        )
    )
    return cursor.fetchall()
