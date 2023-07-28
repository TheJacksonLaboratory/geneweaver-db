"""Database functions for geneset values."""
from typing import List

from geneweaver.core.schema.batch import GenesetValueInput
from geneweaver.db.exceptions import GeneweaverTypeError
from psycopg import Cursor


def format_geneset_values_for_file_insert(
    geneset_values: List[GenesetValueInput],
) -> str:
    """Format geneset values for insertion into the database.

    :param geneset_values: List of geneset values to insert.
    :return: A string to insert into the database.
    """
    return "\n".join(
        (
            f"{geneset_value.symbol}\t{geneset_value.value}"
            for geneset_value in geneset_values
        )
    )


def insert_file(
    cursor: Cursor, formatted_geneset_values: str, comments: str = ""
) -> int:
    """Insert a file of geneset values into the database.

    :param cursor: The database cursor.
    :param formatted_geneset_values: A string formatted version of the geneset values.
    See the `format_geneset_values_for_file_insert` for formatting requirements.
    :param comments: misc. comments about this file

    :raises GeneweaverTypeError: If the geneset values are not a string or are empty.

    :return: The file ID of the inserted file.
    """
    if (
        not isinstance(formatted_geneset_values, str)
        or len(formatted_geneset_values) == 0
    ):
        raise GeneweaverTypeError("Geneset values must be a nonzero length string.")

    cursor.execute(
        """
        INSERT INTO file
            (file_size, file_contents, file_comments, file_created)
        VALUES
            (%s, %s, %s, NOW())
        RETURNING file_id;
        """,
        (len(formatted_geneset_values), formatted_geneset_values, comments),
    )

    cursor.connection.commit()

    return cursor.fetchone()[0]


def get_file(cursor: Cursor, file_id: int) -> str:
    """Retrieve the file contents of a geneset.

    :param cursor: The database cursor.
    :param file_id: File ID associated with a geneset

    :return: A string formatted version of the geneset values. An empty string if the
    file does not exist.
    """
    cursor.execute(
        """
        SELECT file_contents FROM file WHERE file_id = %(file_id)s;
        """,
        {"file_id": file_id},
    )
    contents = cursor.fetchone()

    if not contents:
        return ""

    return contents[0]


def insert_geneset_value(
    cursor: Cursor,
    geneset_id: int,
    gene_id: int,
    value: str,
    name: str,
    within_threshold: bool,
) -> int:
    """Insert a geneset value into the database.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to insert the value into.
    :param gene_id: The gene ID (ode_gene_id) to insert the value into.
    :param value: The value associated with this gene.
    :param name: A gene name or symbol (typically an ode_ref_id).
    :param within_threshold: Whether the value is within the threshold.

    :return: The geneset value ID of the inserted value.
    """
    cursor.execute(
        """
        INSERT INTO geneset_value

            (gs_id, ode_gene_id, gsv_value, gsv_source_list,
            gsv_value_list, gsv_in_threshold, gsv_hits, gsv_date)

        VALUES

            (%s, %s, %s, %s, %s, %s, 0, NOW())

        RETURNING gs_id;
        """,
        (geneset_id, gene_id, value, [name], [float(value)], within_threshold),
    )

    cursor.connection.commit()

    return cursor.fetchone()[0]
