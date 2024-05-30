"""Geneset database functions."""

from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, GenesetTier, ScoreType, Species
from geneweaver.core.schema.gene import GeneValue
from geneweaver.core.schema.geneset import GenesetUpload
from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query import geneset as geneset_query
from geneweaver.db.query.geneset.utils import geneset_upload_to_kwargs
from geneweaver.db.utils import GenesetTierOrTiers, temp_override_row_factory
from psycopg import Cursor, rows
from psycopg.rows import Row


def get(
    cursor: Cursor,
    is_readable_by: Optional[int] = None,
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
    with_publication_info: bool = True,
    ontology_term: Optional[str] = None,
    score_type: Optional[ScoreType] = None,
) -> List[Row]:
    """Get genesets from the database.

    :param cursor: A database cursor.
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
    :param ontology_term: Show only results associated with this ontology term.
    :param score_type: Show only results with given score type.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
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

    return cursor.fetchall()


def by_id(
    cursor: Cursor,
    gs_id: int,
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> Optional[Row]:
    """Get a geneset by its ID.

    :param cursor: A database cursor.
    :param gs_id: The geneset ID to search for.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.
    """
    cursor.execute(
        *geneset_query.get(
            gs_id=gs_id,
            is_readable_by=is_readable_by,
            with_publication_info=with_publication_info,
        )
    )

    return cursor.fetchone()


def by_owner_id(
    cursor: Cursor,
    owner_id: int,
    is_readable_by: Optional[int] = None,
    with_publication_info: bool = True,
) -> List[Row]:
    """Get genesets by owner ID.

    :param cursor: A database cursor.
    :param owner_id: The owner ID to search for.
    :param is_readable_by: A user ID to check if the user can read the results.
    :param with_publication_info: Include publication info in the return.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        *geneset_query.get(
            owner_id=owner_id,
            is_readable_by=is_readable_by,
            with_publication_info=with_publication_info,
        )
    )
    return cursor.fetchall()


def by_project_id(
    cursor: Cursor,
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
    cursor.execute(
        *geneset_query.by_project_id(
            project_id=project_id,
            is_readable_by=is_readable_by,
            with_publication_info=with_publication_info,
        )
    )
    return cursor.fetchall()


def add_geneset(
    cursor: Cursor,
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

    NOTE: This function _only_ adds the geneset file to the database, and does not
    perform any of the required related tasks for new genesets. You most likely *do not*
    want to use this function.

    If you are adding a new geneset, you should use the `add` function instead.

    :param cursor: A database cursor.
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
    :return:
    """
    cursor.execute(
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
    return cursor.fetchone()


def add_geneset_file(
    cursor: Cursor,
    values: List[GeneValue],
    comments: str = "",
) -> Optional[Row]:
    """Add a geneset file to the database.

    NOTE: This function _only_ adds the geneset file to the database, and does not
    perform any of the required related tasks for new genesets. You most likely *do not*
    want to use this function.

    If you are adding a new geneset, you should use the `add` function instead.

    :param cursor: A database cursor.
    :param values: A list of GeneValues to render into a file.
    :param comments: Comments to include with the file.
    :return: The ID of the added file.
    """
    cursor.execute(
        *geneset_query.add_geneset_file(
            values=values,
            comments=comments,
        )
    )

    return cursor.fetchone()


def add(
    cursor: Cursor,
    geneset: GenesetUpload,
    owner_id: Optional[int] = None,
    publication_id: Optional[int] = None,
) -> int:
    """Add a geneset to the database with all necessary components.

    :param cursor: A database cursor.
    :param geneset: An instance of a GenesetUpload schema.
    :param owner_id: The owner of the geneset.
    :param publication_id: The (internal) publication ID associated with the Geneset.
    :return: The geneset ID.
    """
    file_id = add_geneset_file(
        cursor=cursor,
        values=geneset.gene_list,
    )
    geneset_id = add_geneset(
        cursor=cursor,
        user_id=owner_id,
        file_id=file_id,
        publication_id=publication_id,
        **geneset_upload_to_kwargs(geneset)
    )
    cursor.execute(*geneset_query.reparse_geneset_file(geneset_id=geneset_id))
    cursor.execute(*geneset_query.process_thresholds(geneset_id=geneset_id))
    return geneset_id


# --------------------------------------------------------------------------------------
# The following functions are not yet implemented in the aio/concurrent paradigm.
# They are subject to change and may be deprecated in the future.


@temp_override_row_factory(rows.tuple_row)
def is_readable(cursor: Cursor, user_id: int, geneset_id: int) -> bool:
    """Check if a geneset is readable by a user.

    :param cursor: The database cursor.
    :param user_id: The user id (internal) to check.
    :param geneset_id: The geneset id to check.

    :return: True if the geneset is readable by the user, False otherwise.
    """
    cursor.execute(
        """
        SELECT production.geneset_is_readable2(%(user_id)s, %(geneset_id)s);
        """,
        {"user_id": user_id, "geneset_id": geneset_id},
    )
    return cursor.fetchone()[0] is True


@temp_override_row_factory(rows.tuple_row)
def user_is_owner(cursor: Cursor, user_id: int, geneset_id: int) -> bool:
    """Check if a user is the owner of a geneset.

    :param cursor: The database cursor.
    :param user_id: The user id (internal) to check.
    :param geneset_id: The geneset id to check.

    :return: True if the user is the owner of the geneset, False otherwise.
    """
    cursor.execute(
        """
        SELECT COUNT(gs_id) FROM geneset
        WHERE usr_id=%(user_id)s AND gs_id=%(geneset_id)s;
        """,
        {"user_id": user_id, "geneset_id": geneset_id},
    )
    result = cursor.fetchone()[0]
    return result == 1 and not isinstance(result, bool)


@temp_override_row_factory(rows.tuple_row)
def update_date(cursor: Cursor, geneset_id: int) -> str:
    """Update the date of a geneset.

    :param cursor: The database cursor.
    :param geneset_id: The geneset id to update.

    :return: The updated date.
    """
    cursor.execute(
        """
        UPDATE geneset SET gs_updated = NOW()
        WHERE gs_id = %(geneset_id)s
        RETURNING gs_updated
        """,
        {"geneset_id": geneset_id},
    )
    cursor.connection.commit()
    return cursor.fetchone()[0]


@temp_override_row_factory(rows.tuple_row)
def tier(cursor: Cursor, geneset_id: int) -> Optional[int]:
    """Get the tier of a geneset.

    :param cursor: The database cursor.
    :param geneset_id: The geneset id to get the tier of.

    :return: The tier of the geneset, or None if the geneset does not have a tier,
    or does not exist.
    """
    cursor.execute(
        """
        SELECT cur_id FROM geneset WHERE gs_id = %(geneset_id)s;
        """,
        {"geneset_id": geneset_id},
    )
    result = cursor.fetchone()

    if not result:
        return None

    return result[0]


def homology_ids(cursor: Cursor, geneset_id: int) -> List:
    """Get all homology_ids that are associated with a geneset ID.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        SELECT DISTINCT hom_id FROM extsrc.homology h
        INNER JOIN extsrc.geneset_value gsv
            ON h.ode_gene_id=gsv.ode_gene_id
        INNER JOIN production.geneset g
            ON gsv.gs_id=g.gs_id
        WHERE gs_status not like 'de%%' AND g.gs_id=%(geneset_id)s""",
        {"geneset_id": geneset_id},
    )
    return cursor.fetchall()


# TODO: reimplement `get_all_geneset_values`


@temp_override_row_factory(rows.tuple_row)
def num_genes(cursor: Cursor, geneset_id: int) -> int:
    """Get the number of genes associated with a geneset ID.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to search for.

    :return: The number of genes associated with the geneset ID.
    """
    cursor.execute(
        """
        SELECT COUNT(*) FROM extsrc.geneset_value WHERE gs_id = %(geneset_id)s;
        """,
        {"geneset_id": geneset_id},
    )
    return cursor.fetchone()[0]
