"""Async database interaction code relating to Genesets."""

from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, ScoreType, Species
from geneweaver.db.query import geneset as geneset_query
from geneweaver.db.utils import GenesetTierOrTiers
from psycopg import AsyncCursor
from psycopg.rows import Row


async def get(
    cursor: AsyncCursor,
    gs_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    curation_tier: Optional[GenesetTierOrTiers] = None,
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
    ontology_term: Optional[str] = None,
    score_type: Optional[ScoreType] = None,
) -> List[Row]:
    """Get genesets from the database.

    :param cursor: An async database cursor.
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
    :param ontology_term: Show only results associated with this ontology term.
    :param score_type: Show only results with given score type.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(
        *geneset_query.get(
            is_readable_by=is_readable_by,
            gs_id=gs_id,
            owner_id=owner_id,
            curation_tier=curation_tier,
            species=species,
            name=name,
            abbreviation=abbreviation,
            publication_id=publication_id,
            pubmed_id=pubmed_id,
            gene_id_type=gene_id_type,
            search_text=search_text,
            limit=limit,
            offset=offset,
            with_publication_info=with_publication_info,
            ontology_term=ontology_term,
            score_type=score_type,
        )
    )

    return await cursor.fetchall()


async def by_id(
    cursor: AsyncCursor,
    gs_id: int,
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> Optional[Row]:
    """Get a geneset by its ID.

    :param cursor: An async database cursor.
    :param gs_id: The geneset ID to search for.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.
    """
    await cursor.execute(
        *geneset_query.get(
            gs_id=gs_id,
            is_readable_by=is_readable_by,
            with_publication_info=with_publication_info,
        )
    )

    return await cursor.fetchone()


async def by_owner_id(
    cursor: AsyncCursor,
    owner_id: int,
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> List[Row]:
    """Get genesets by owner ID.

    :param cursor: An async database cursor.
    :param owner_id: The owner ID to search for.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(
        *geneset_query.get(
            owner_id=owner_id,
            is_readable_by=is_readable_by,
            with_publication_info=with_publication_info,
        )
    )
    return await cursor.fetchall()


async def by_project_id(
    cursor: AsyncCursor,
    project_id: int,
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> List[Row]:
    """Get a list of genesets by their membership in a project.

    :param cursor: An async database cursor.
    :param project_id: The project ID to search for.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(
        *geneset_query.by_project_id(
            project_id=project_id,
            is_readable_by=is_readable_by,
            with_publication_info=with_publication_info,
        )
    )
    return await cursor.fetchall()
