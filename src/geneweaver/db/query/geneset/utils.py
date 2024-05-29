"""Utility functions for the geneset query."""

from typing import Optional, Tuple

from geneweaver.core.enum import GenesetTier
from geneweaver.core.schema.geneset import GenesetUpload
from geneweaver.db.query.geneset.const import (
    GENESET_FIELDS,
    GENESET_TSVECTOR,
    PUB_FIELDS,
)
from geneweaver.db.query.search import utils
from geneweaver.db.query.utils import (
    ParamDict,
    SQLList,
)
from geneweaver.db.utils import GenesetTierOrTiers
from psycopg.sql import SQL, Composed


def format_select_query(
    with_publication_info: bool = False,
    with_publication_join: bool = False,
) -> Composed:
    """Format the geneset query.

    Construct the geneset query with appropriate fields and joins.

    If the `with_publication_info` flag is set to True, the query will include the
    publication table for querying AND return data. When `with_publication_info` is set
    to True, the `with_publication_join` option is ignored.

    If the `with_publication_join` flag is set to True, the query will include
    the publication table for querying, but not return. This option is ignored if the
    `with_publication_info` flag is set to True.

    :param with_publication_info: Whether to include publication info in return.
    :param with_publication_join: Whether to include publication for querying.

    :return: The formatted query.
    """
    query = SQL("SELECT")
    if with_publication_info:
        query = (
            query
            + SQL(",").join(GENESET_FIELDS + PUB_FIELDS)
            + SQL("FROM geneset LEFT OUTER JOIN publication")
            + SQL("ON geneset.pub_id = publication.pub_id")
        )
    elif with_publication_join:
        query = (
            query
            + SQL(",").join(GENESET_FIELDS)
            + SQL("FROM geneset LEFT OUTER JOIN publication")
            + SQL("ON geneset.pub_id = publication.pub_id")
        )
    else:
        query = query + SQL(",").join(GENESET_FIELDS) + SQL("FROM geneset")
    return query


def add_ontology_query(query: Composed) -> Composed:
    """Expand geneset query with join to ontology.

    :param query: geneset base query
    """
    ontology_query = (
        query
        + SQL("JOIN geneset_ontology ON geneset.gs_id = geneset_ontology.gs_id")
        + SQL("JOIN ontology ON geneset_ontology.ont_id = ontology.ont_id")
    )

    return ontology_query


def add_ontology_parameter(
    existing_filters: SQLList, existing_params: ParamDict, ontology_term: str
) -> Tuple[SQLList, ParamDict]:
    """Add the ontology term filter to the query.

    :param existing_filters: The existing filters.
    :param existing_params: The existing parameters.
    :param ontology_term: The ontology term to filter by.
    """
    existing_filters.append(SQL("ontology.ont_ref_id IN(%(ontology_term)s)"))
    existing_params["ontology_term"] = ontology_term
    return existing_filters, existing_params


def is_readable(
    existing_filters: SQLList,
    existing_params: ParamDict,
    is_readable_by: Optional[int] = None,
) -> Tuple[SQLList, ParamDict]:
    """Add the is_readable filter to the query.

    :param existing_filters: The existing filters.
    :param existing_params: The existing parameters.
    :param is_readable_by: The user ID to filter by.
    """
    if is_readable_by is not None:
        existing_filters.append(
            SQL("production.geneset_is_readable2(%(is_readable_by)s, geneset.gs_id)")
        )
        existing_params["is_readable_by"] = is_readable_by
    return existing_filters, existing_params


def search(
    existing_filters: SQLList,
    existing_params: ParamDict,
    search_text: Optional[str] = None,
) -> Tuple[SQLList, ParamDict]:
    """Add the search filter to the query.

    :param existing_filters: The existing filters.
    :param existing_params: The existing parameters.
    :param search_text: The search text to filter by.
    """
    if search_text is not None:
        search_sql, search_params = utils.search_query(GENESET_TSVECTOR, search_text)
        existing_filters.append(search_sql)
        existing_params.update(search_params)
    return existing_filters, existing_params


def restrict_tier(
    existing_filters: SQLList,
    existing_params: ParamDict,
    curation_tier: Optional[GenesetTierOrTiers] = None,
) -> Tuple[SQLList, ParamDict]:
    """Restrict the query by curation tier.

    :param existing_filters: The existing filters.
    :param existing_params: The existing parameters.
    :param curation_tier: The curation tier to filter by.
    """
    if isinstance(curation_tier, GenesetTier):
        curation_tier = {curation_tier}
    if curation_tier is not None:
        existing_filters.append(SQL("geneset.cur_id = ANY(%(curation_tier)s)"))
        existing_params["curation_tier"] = [int(tier) for tier in curation_tier]
    return existing_filters, existing_params


def geneset_upload_to_kwargs(geneset: GenesetUpload) -> dict:
    """Turn a GenesetUpload into a dict to be used as kwargs for SQL functions.

    :param geneset: The geneset to process.
    :return: A dict of the SQL function kwargs for adding a geneset.
    """
    tier = GenesetTier.TIER4 if geneset.private is not True else GenesetTier.TIER5
    return {
        "name": geneset.name,
        "abbreviation": geneset.abbreviation,
        "tier": tier,
        "species": geneset.species,
        "count": len(geneset.values),
        "score": geneset.score,
        "gene_id_type": geneset.gene_id_type,
        "description": geneset.description,
    }
