"""SQL query generation code for writing genesets."""

from typing import List, Optional, Tuple

from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.core.schema.gene import GeneValue
from geneweaver.core.schema.score import GenesetScoreType
from psycopg.sql import SQL, Composed


def add(
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
) -> Tuple[Composed, dict]:
    """Add a geneset to the database.

    :param user_id: The user ID of the geneset owner.
    :param file_id: The file ID of the geneset file.
    :param name: The name of the geneset.
    :param abbreviation: The abbreviation of the geneset.
    :param publication_id: The publication ID of the geneset.
    :param tier: The curation tier of the geneset.
    :param description: The description of the geneset.
    :param species: The species of the geneset.
    :param count: The count of the geneset.
    :param score: The threshold type and amount of the geneset.
    :param gene_id_type: The gene ID type of the geneset.
    :param attribution: The attribution of the geneset.

    :return: A query (and params) that can be executed on a cursor.
    """
    query_cols = SQL(
        """
        (usr_id, file_id, gs_name, gs_abbreviation, pub_id, cur_id,
        gs_description, sp_id, gs_count, gs_threshold_type,
        gs_threshold, gs_groups, gs_gene_id_type, gs_created,
        gs_attribution)
    """
    )
    query_vals = SQL(
        """
        VALUES
        (%(usr_id)s, %(file_id)s, %(gs_name)s, %(gs_abbreviation)s,
        %(pub_id)s, %(cur_id)s, %(gs_description)s, %(sp_id)s,
        %(gs_count)s, %(gs_threshold_type)s, %(gs_threshold)s,
        %(gs_groups)s, %(gs_gene_id_type)s, %(gs_created)s,
        %(gs_attribution)s
    """
    )

    query = (
        SQL("INSERT INTO geneset") + query_cols + query_vals + SQL("RETURNING gs_id")
    ).join(" ")

    params = {
        "usr_id": user_id,
        "file_id": file_id,
        "gs_name": name,
        "gs_abbreviation": abbreviation,
        "pub_id": publication_id,
        "cur_id": int(tier),
        "gs_description": description,
        "sp_id": int(species),
        "gs_count": count,
        "gs_threshold_type": int(score.score_type),
        "gs_threshold": score.threshold_as_db_string(),
        "gs_groups": "",
        "gs_gene_id_type": int(gene_id_type),
        "gs_created": "NOW()",
        "gs_attribution": attribution,
    }

    return query, params


def add_geneset_file(
    values: List[GeneValue],
    comments: str = "",
) -> Tuple[Composed, dict]:
    """Render and add a geneset file to the database.

    This function takes a list of gene values and renders them into a string
    that can be added to the database as a geneset file.

    :param values: The gene values to render.
    :param comments: The comments for the file.
    :return: A query (and params) that can be executed on a cursor.
    """
    contents = "\n".join(f"{value.symbol}\t{value.value}" for value in values)
    size = len(contents)
    return add_geneset_file_raw(size, contents, comments)


def add_geneset_file_raw(
    size: int,
    contents: str,
    comments: str,
) -> Tuple[Composed, dict]:
    """Add a geneset file to the database.

    :param size: The size of the file.
    :param contents: The contents of the file.
    :param comments: The comments for the file.
    :return: A query (and params) that can be executed on a cursor.
    """
    query = (
        SQL("INSERT INTO file")
        + SQL("(file_size, file_contents, file_comments, file_created)")
        + SQL("VALUES (%(file_size)s, %(file_contents)s, %(file_comments)s, NOW())")
        + SQL("RETURNING file_id")
    ).join(" ")
    params = {"file_size": size, "file_contents": contents, "file_comments": comments}
    return query, params


def reparse_geneset_file(geneset_id: int) -> Tuple[Composed, dict]:
    """Call the `reparse_geneset_file` function in the database.

    :param geneset_id: The ID of the geneset to reparse.
    :return: A query (and params) that can be executed on a cursor.
    """
    query = (
        SQL("SELECT")
        + SQL("production.reparse_geneset_file($(reparse_geneset_file__geneset_id));")
    ).join(" ")
    params = {"reparse_geneset_file__geneset_id": geneset_id}
    return query, params


def process_thresholds(geneset_id: int) -> Tuple[Composed, dict]:
    """Call the `process_thresholds` function in the database.

    :param geneset_id: The ID of the geneset to process.
    :return: A query (and params) that can be executed on a cursor.
    """
    query = (
        SQL("SELECT")
        + SQL("production.process_thresholds($(process_thresholds__geneset_id));")
    ).join(" ")
    params = {"process_thresholds__geneset_id": geneset_id}
    return query, params
