"""Database functions for geneset values."""
from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier
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


def by_geneset_id(
    cursor: Cursor, geneset_id: int, identifier: Optional[GeneIdentifier] = None
) -> list:
    """Retrieve all geneset values associated with a geneset.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to retrieve values for.
    :param identifier: The gene identifier to return.

    :return: A list of geneset values associated with the geneset.
    """
    if identifier is not None:
        return by_geneset_id_and_identifier(cursor, geneset_id, identifier)
    else:
        return by_geneset_id_as_uploaded(cursor, geneset_id)


def by_geneset_id_as_uploaded(cursor: Cursor, geneset_id: int) -> list:
    """Retrieve all geneset values associated with a geneset.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to retrieve values for.

    :return: A list of geneset values associated with the geneset.
    """
    cursor.execute(
        """
        SELECT DISTINCT ON (gv.ode_gene_id) gv.*, g.ode_ref_id
        FROM        extsrc.geneset_value gv
        INNER JOIN  extsrc.gene g
        USING       (ode_gene_id)
        WHERE  gs_id = %(geneset_id)s;
        """,
        {"geneset_id": geneset_id},
    )
    return cursor.fetchall()


def by_geneset_id_and_identifier(
    cursor: Cursor, geneset_id: int, identifier: GeneIdentifier
) -> list:
    """Retrieve all geneset values associated with a geneset.

    NOTE: If you are mapping identifiers across species, you will need to use the
    `geneweaver.db.gene.get_homolog_ids_by_ode_id` function to get the homolog ids
    for the geneset values after processing the results of this function.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to retrieve values for.
    :param identifier: The gene identifier to use.

    :return: A list of geneset values associated with the geneset.
    """
    cursor.execute(
        """
            SELECT gsv.gs_id, gsv.ode_gene_id, gsv.gsv_value, gsv.gsv_hits,
                   gsv.gsv_source_list, gsv.gsv_value_list,
                   gsv.gsv_in_threshold, gsv.gsv_date, h.hom_id, gi.gene_rank,
                   gsv.ode_ref_id, gsv.gdb_id

            --
            -- Use a subquery here so we can prevent duplicate gene identifiers
            -- of the same type from being returned (the DISTINCT ON section)
            -- otherwise when we try to change identifier types from the view
            -- GS page, duplicate entries screw things up
            --
            FROM (
                SELECT DISTINCT ON (g.ode_gene_id, g.gdb_id)
                        gsv.*, g.ode_ref_id, g.gdb_id, g.ode_pref
                FROM    geneset_value as gsv, gene as g
                WHERE   gsv.gs_id = %(geneset_id)s AND
                        g.ode_gene_id = gsv.ode_gene_id AND
                        g.gdb_id = (SELECT COALESCE (
                            (SELECT gdb_id
                             FROM   gene AS g2
                             WHERE g2.ode_gene_id = gsv.ode_gene_id AND
                                   g2.gdb_id = %(gdb_id)s
                             LIMIT 1),
                            (SELECT gdb_id
                             FROM   gene AS g2
                             WHERE g2.ode_gene_id = gsv.ode_gene_id AND
                                   g2.gdb_id = 7
                             LIMIT 1)
                        )) AND

                        --
                        -- When viewing symbols, always pick the preferred gene symbol
                        --
                        CASE
                            WHEN g.gdb_id = 7 THEN g.ode_pref = 't'
                            ELSE true
                        END
            ) gsv

            --
            -- gene_info necessary for the priority scores
            --
            INNER JOIN  gene_info AS gi
            ON          gsv.ode_gene_id = gi.ode_gene_id

            --
            -- Have to use a left outer join because some genes may not have homologs
            --
            LEFT OUTER JOIN homology AS h
            ON          gsv.ode_gene_id = h.ode_gene_id

            WHERE h.hom_source_name = 'Homologene' OR
                  -- In case the gene doesn't have any homologs
                  h.hom_source_name IS NULL
        """,
        {"geneset_id": geneset_id, "gdb_id": identifier.value},
    )
    return cursor.fetchall()
