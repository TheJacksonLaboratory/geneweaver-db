from typing import Iterable, Tuple, Optional, Dict, Union

from psycopg.sql import SQL, Composed
from geneweaver.db.query.publication import PUB_FIELD_MAP
from geneweaver.db.utils import format_sql_fields, limit_and_offset
from geneweaver.db.query.search import utils
from geneweaver.db.query.utils import (
    construct_filters,
    ParamDict,
    OptionalParamDict,
    SQLList,
)

from geneweaver.core.enum import GenesetTier, Species, GeneIdentifier


GENESET_FIELDS_MAP = {
    "gs_id": "id",
    "usr_id": "user_id",
    "file_id": "file_id",
    "cur_id": "curation_id",
    "sp_id": "species_id",
    "gs_name": "name",
    "gs_abbreviation": "abbreviation",
    "pub_id": "publication_id",
    "gs_description": "description",
    "gs_count": "count",
    "gs_threshold_type": "score_type",
    "gs_threshold": "threshold",
    "gs_status": "status",
    "gs_gene_id_type": "gene_id_type",
    "gs_attribution": "attribution",
    "gs_created": "created",
    "gs_updated": "updated",
}

GENESET_FIELDS = format_sql_fields(GENESET_FIELDS_MAP, query_table="geneset")
PUB_FIELDS = format_sql_fields(
    PUB_FIELD_MAP, query_table="publication", resp_prefix="publication"
)
GENESET_TSVECTOR = "geneset.gs_tsvector"


def get(
    is_readable_by: Optional[int] = None,
    gs_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    curation_tier: Optional[GenesetTier] = None,
    species: Optional[Species] = None,
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    publication_id: Optional[int] = None,
    pubmed_id: Optional[int] = None,
    gene_id_type: Optional[GeneIdentifier] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    with_publication_info: bool = True,
) -> Tuple[Composed, dict]:
    """Get genesets.

    :param is_readable_by: A user ID to check if the user can read the results.
    :param gs_id: Show only results with this geneset ID.
    :param owner_id: Show only results owned by this user ID.
    :param curation_tier: Show only results of this curation tier.
    :param species: Show only results associated with this species.
    :param name: Show only results with this name.
    :param abbreviation: Show only results with this abbreviation.
    :param publication_id: Show only results with this publication ID (internal).
    :param pubmed_id: Show only results with this PubMed ID.
    :param gene_id_type: Show only results with this gene ID type.
    :param search_text: Return genesets that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :param with_publication_info: Include publication info in the return.
    """
    params = {}
    filtering = []
    query = format_select_query(with_publication_info=with_publication_info,
                                with_publication_join=pubmed_id is not None)

    filtering, params = is_readable(filtering, params, is_readable_by)
    filtering, params = search(filtering, params, search_text)

    filtering, params = construct_filters(
        filtering,
        params,
        {
            "gs_id": gs_id,
            "usr_id": owner_id,
            "cur_id": int(curation_tier) if curation_tier is not None else None,
            "sp_id": int(species) if species is not None else None,
            "gs_name": name,
            "gs_abbreviation": abbreviation,
            "pub_id": publication_id,
            "publication.pubmed_id": pubmed_id,
            "gs_gene_id_type": int(gene_id_type) if gene_id_type is not None else None,
        },
    )

    if len(filtering) > 0:
        query += SQL("WHERE") + SQL("AND").join(filtering)

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params


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
            + SQL(",").join(GENESET_FIELDS) + SQL("FROM geneset")
            + SQL("FROM geneset LEFT OUTER JOIN publication")
            + SQL("ON geneset.pub_id = publication.pub_id")
        )
    else:
        query = query + SQL(",").join(GENESET_FIELDS) + SQL("FROM geneset")
    return query


def is_readable(
    existing_filters: SQLList,
    existing_params: ParamDict,
    is_readable_by: Optional[int] = None,
) -> Tuple[SQLList, ParamDict]:
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
    if search_text is not None:
        search_sql, search_params = utils.search_query(GENESET_TSVECTOR, search_text)
        existing_filters.append(search_sql)
        existing_params.update(search_params)
    return existing_filters, existing_params
