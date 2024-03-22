"""SQL query generation code for reading genesets."""

from typing import Optional, Tuple

from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.db.query.geneset.utils import (
    format_select_query,
    is_readable,
    search,
)
from geneweaver.db.query.utils import construct_filters
from geneweaver.db.utils import limit_and_offset
from psycopg.sql import SQL, Composed


def get(
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
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> Tuple[Composed, dict]:
    """Get genesets.

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
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.
    """
    params = {}
    filtering = []
    query = format_select_query(
        with_publication_info=with_publication_info,
        with_publication_join=pubmed_id is not None,
    )

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


def by_project_id(
    project_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> Tuple[Composed, dict]:
    """Create a psycopg query to get genesets by project ID.

    :param project_id: The project ID to search for.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = (
        format_select_query(with_publication_info=with_publication_info)
        + SQL("JOIN project_geneset ON geneset.gs_id = project_geneset.gs_id")
        + SQL("INNER JOIN production.project2geneset")
        + SQL("ON geneset.gs_id=project2geneset.gs_id")
        + SQL("WHERE project2geneset.pj_id=%(project_id)s")
    )
    params = {"project_id": project_id}
    filtering, params = is_readable([], params, is_readable_by)

    if len(filtering) > 0:
        query += SQL("WHERE") + SQL("AND").join(filtering)
    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params
