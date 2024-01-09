"""Database interaction code relating to Gene IDs."""
from typing import Iterable, List, Optional

from geneweaver.core.enum import GeneIdentifier
from psycopg import Cursor


def id_types(cursor: Cursor, species_id: Optional[int] = None) -> List:
    """Get all the Gene ID types from the database.

    :param cursor: The database cursor.
    :param species_id: Limit to additional species other than mouse

    :return: list of results using `.fetchall()`
    """
    if species_id is None:
        cursor.execute("""SELECT * FROM odestatic.genedb ORDER BY gdb_id;""")
    else:
        cursor.execute(
            """SELECT * FROM odestatic.genedb
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


def gene_database_id(cursor: Cursor, identifier: GeneIdentifier) -> List:
    """Get all gene database info by gene database name.

    :param cursor: The database cursor.
    :param identifier: The gene database name to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT gdb_id FROM odestatic.genedb WHERE gdb_shortname = %(gdb_name)s;""",
        {"gdb_name": identifier.name.lower},
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


def get_homolog_ids_by_ode_id(
    cursor: Cursor, ode_gene_ids: Iterable[str], identifier: GeneIdentifier
) -> List:
    """Get all homolog ids associated with a specific gene id.

    :param cursor: The database cursor.
    :param ode_gene_ids: The gene ids to search for.
    :param identifier: The identifier to return genes in.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        SELECT DISTINCT     h.ode_gene_id, g.ode_ref_id
        FROM                homology AS h
        INNER JOIN          homology AS h2
        ON                  h.hom_id = h2.hom_id
        INNER JOIN          gene AS g
        ON                  g.ode_gene_id = h2.ode_gene_id
        WHERE               h.ode_gene_id in %(ode_gene_ids)s AND
                            g.gdb_id = %(genedb_id)s;
        """,
        {"ode_gene_ids": tuple(ode_gene_ids), "genedb_id": identifier.value},
    )
    return cursor.fetchall()


def get_homolog_ids(
    cursor: Cursor,
    source_ids: Iterable[str],
    result_identifier: GeneIdentifier,
    source_identifier: Optional[GeneIdentifier] = None,
) -> list:
    """Get homologous GeneIDs for a list of source IDs.

    :param cursor: The database cursor.
    :param source_ids: The gene ids to search for.
    :param result_identifier: The identifier to return genes in.
    :param source_identifier: The identifier to search for genes in (optional).
    """
    if source_identifier is not None:
        return get_homolog_ids_with_source_identifier(
            cursor,
            source_ids,
            result_identifier=result_identifier,
            source_identifier=source_identifier,
        )
    else:
        return get_homolog_ids_without_source_identifier(
            cursor, source_ids, result_identifier=result_identifier
        )


def get_homolog_ids_with_source_identifier(
    cursor: Cursor,
    source_ids: Iterable[str],
    result_identifier: GeneIdentifier,
    source_identifier: GeneIdentifier,
) -> list:
    """Get homologous GeneIDs for a list of source IDs.

    :param cursor: The database cursor.
    :param source_ids: The gene ids to search for.
    :param result_identifier: The identifier to return genes in.
    :param source_identifier: The identifier to search for genes in (optional).
    """
    cursor.execute(
        """
        SELECT DISTINCT result_gene.ode_ref_id, source_gene.ode_ref_id
        FROM homology AS source_homology
            INNER JOIN homology AS result_homology
                ON source_homology.hom_id = result_homology.hom_id
            INNER JOIN gene AS result_gene
                ON result_gene.ode_gene_id = result_homology.ode_gene_id
            INNER JOIN gene AS source_gene
                ON source_gene.ode_gene_id = source_homology.ode_gene_id
        WHERE result_gene.gdb_id = %(result_genedb_id)s
            AND source_gene.gdb_id = %(source_genedb_id)s
            AND source_gene.ode_ref_id IN %(source_ids)s;
        """,
        {
            "result_genedb_id": result_identifier.value,
            "source_genedb_id": source_identifier.value,
            "source_ids": tuple(source_ids),
        },
    )
    return cursor.fetchall()


def get_homolog_ids_without_source_identifier(
    cursor: Cursor, source_ids: Iterable[str], result_identifier: GeneIdentifier
) -> list:
    """Get homologous GeneIDs for a list of source IDs.

    :param cursor: The database cursor.
    :param source_ids: The gene ids to search for.
    :param result_identifier: The identifier to return genes in.
    """
    cursor.execute(
        """
        SELECT DISTINCT result_gene.ode_ref_id, source_gene.ode_ref_id
        FROM homology AS source_homology
            INNER JOIN homology AS result_homology
                ON source_homology.hom_id = result_homology.hom_id
            INNER JOIN gene AS result_gene
                ON result_gene.ode_gene_id = result_homology.ode_gene_id
            INNER JOIN gene AS source_gene
                ON source_gene.ode_gene_id = source_homology.ode_gene_id
        WHERE result_gene.gdb_id = %(result_genedb_id)s
            AND source_gene.ode_ref_id IN %(source_ids)s;
        """,
        {"result_genedb_id": result_identifier.value, "source_ids": tuple(source_ids)},
    )
    return cursor.fetchall()
