"""Async database interaction code relating to Genesets."""

from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, GenesetTier, ScoreType, Species
from geneweaver.core.schema.gene import GeneValue
from geneweaver.core.schema.geneset import GenesetUpload
from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query import geneset as geneset_query
from geneweaver.db.query.geneset.utils import geneset_upload_to_kwargs
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


async def add_geneset(
    cursor: AsyncCursor,
    user_id: int,
    file_id: int,
    name: str,
    abbreviation: str,
    tier: GenesetTier,
    species: Species,
    count: int,
    score: GenesetScoreType,
    gene_id_type: GeneIdentifier,
    description: str = "",
    publication_id: Optional[int] = None,
    attribution: Optional[str] = None,
) -> Optional[Row]:
    """Add a geneset to the database.

    NOTE: This function _only_ adds the geneset instance to the database, and does not
    perform any of the required related tasks for new genesets. You most likely *do not*
    want to use this function.

    If you are adding a new geneset, you should use the `add` function instead.

    :param cursor: An async database cursor.
    :param user_id: The owner of the geneset.
    :param file_id: The file ID of the geneset's values.
    :param name: The name of the geneset.
    :param abbreviation: The abbreviation of the geneset.
    :param tier: The curation tier of the geneset.
    :param species: The species of the geneset.
    :param count: The number of genes in the geneset.
    :param score: The score of the geneset (GenesetScoreType includes threshold info).
    :param gene_id_type: The gene ID type of the geneset.
    :param description: The description of the geneset.
    :param publication_id: The publication ID of the geneset (not the PubMed ID).
    :param attribution: The attribution of the geneset.
    :return: The ID of the added Geneset using fetchone().
    """
    await cursor.execute(
        *geneset_query.add(
            user_id=user_id,
            file_id=file_id,
            name=name,
            abbreviation=abbreviation,
            tier=tier,
            species=species,
            count=count,
            score=score,
            gene_id_type=gene_id_type,
            description=description,
            publication_id=publication_id,
            attribution=attribution,
        )
    )
    return await cursor.fetchone()


async def add_geneset_file(
    cursor: AsyncCursor,
    values: List[GeneValue],
    comments: str = "",
) -> Optional[Row]:
    """Add a geneset file to the database.

    NOTE: This function _only_ adds the geneset file to the database, and does not
    perform any of the required related tasks for new genesets. You most likely *do not*
    want to use this function.

    If you are adding a new geneset, you should use the `add` function instead.

    :param cursor: An async database cursor.
    :param values: A list of GeneValues to render into a file.
    :param comments: Comments to include with the file.
    :return: The ID of the added file using fetchone().
    """
    await cursor.execute(
        *geneset_query.add_geneset_file(
            values=values,
            comments=comments,
        )
    )

    return await cursor.fetchone()


async def add(
    cursor: AsyncCursor,
    geneset: GenesetUpload,
    owner_id: Optional[int] = None,
    publication_id: Optional[int] = None,
) -> int:
    """Add a geneset to the database with all necessary components.

    :param cursor: An async database cursor.
    :param geneset: An instance of a GenesetUpload schema.
    :param owner_id: The owner of the geneset.
    :param publication_id: The (internal) publication ID associated with the Geneset.
    :return: The geneset ID.
    """
    file_id = await add_geneset_file(
        cursor=cursor,
        values=geneset.gene_list,
    )
    geneset_id = await add_geneset(
        cursor=cursor,
        user_id=owner_id,
        file_id=file_id,
        publication_id=publication_id,
        **geneset_upload_to_kwargs(geneset)
    )
    await cursor.execute(*geneset_query.reparse_geneset_file(geneset_id=geneset_id))
    await cursor.execute(*geneset_query.process_thresholds(geneset_id=geneset_id))
    return geneset_id
