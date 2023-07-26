"""Database interaction code relating to Gene IDs."""
from typing import List, Optional

from psycopg import Cursor


def id_types(cursor: Cursor, species_id: Optional[int] = None) -> List:
    """Get all the Gene ID types from the database.

    :param cursor: The database cursor.
    :param species_id: Limit to additional species other than mouse

    :return: list of results using `.fetchall()`
    """
    if species_id is None:
        cursor.execute("""SELECT * FROM genedb ORDER BY gdb_id;""")
    else:
        cursor.execute(
            """SELECT * FROM genedb
            WHERE sp_id=0 OR sp_id=%(sp_id)s
            ORDER BY gdb_id;""",
            {"sp_id": species_id},
        )

    return cursor.fetchall()


# This SQL might be re-used by other functions, so it's defined here.
# Specifically, postgres has a row_to_json function that is used extensively for the
# GW2 API, and it's possible that we might want to use it here as well.
INFO_BY_GENE_ID_SQL = "SELECT * FROM extsrc.gene_info WHERE ode_gene_id = %(gene_id)s;"


def info_by_gene_id(cursor: Cursor, gene_id: int) -> List:
    """Get Gene ID type info by gene id.

    :param cursor: The database cursor.
    :param gene_id: The gene id to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(INFO_BY_GENE_ID_SQL, {"gene_id": gene_id})
    return cursor.fetchall()


def gene_database_by_id(cursor: Cursor, genedb_id: int) -> List:
    """Get all gene database info by gene database id.

    :param cursor: The database cursor.
    :param genedb_id: The gene database id to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT * FROM odestatic.genedb WHERE gdb_id = %(gdb_id)s;""",
        {"gdb_id": genedb_id},
    )
    return cursor.fetchall()


def symbols_by_geneset_id(cursor: Cursor, geneset_id: int) -> List:
    """Get all gene symbols associated with a specific geneset id.

    :param cursor: The database cursor.
    :param geneset_id: The geneset id to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        SELECT g.ode_ref_id
        FROM extsrc.gene g, extsrc.geneset_value gv
        WHERE gv.gs_id= %(geneset_id)s
        AND gv.ode_gene_id=g.ode_gene_id
        AND g.gdb_id=7
        AND ode_pref='t';
        """,
        {"geneset_id": geneset_id},
    )
    return cursor.fetchall()


def symbols_by_project_id(cursor: Cursor, project_id: int) -> List:
    """Get all gene symbols associated with a specific project id.

    :param cursor: The database cursor.
    :param project_id: The project id to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        SELECT g.ode_ref_id
        FROM extsrc.gene g, extsrc.geneset_value gv
        WHERE (gv.gs_id IN
                (SELECT gs_id AS geneSetId
                FROM production.project2geneset
                WHERE pj_id = %(project_id)s))
        AND gv.ode_gene_id=g.ode_gene_id AND g.gdb_id=7 AND ode_pref='t';
    """,
        {"project_id": project_id},
    )
    return cursor.fetchall()
