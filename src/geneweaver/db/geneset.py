"""Geneset database functions."""
from typing import List, Optional

from psycopg import Cursor, rows


def by_id(cursor: Cursor, geneset_id: int) -> Optional[rows.Row]:
    """Get geneset info by geneset id.

    :param cursor: The database cursor.
    :param geneset_id: The geneset id to search for.

    :return: optional row using `.fetchone()`
    """
    cursor.execute(
        """SELECT * FROM production.geneset WHERE gs_id = %(geneset_id)s;""",
        {"geneset_id": geneset_id},
    )
    return cursor.fetchone()


def by_user_id(cursor: Cursor, user_id: int) -> List:
    """Get geneset info by user id.

    :param cursor: The database cursor.
    :param user_id: The user id (internal) to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT * FROM production.geneset WHERE user_id = %(user_id)s;""",
        {"user_id": user_id},
    )
    return cursor.fetchall()


def by_project_id(cursor: Cursor, project_id: int) -> List:
    """Get geneset info by project id.

    :param cursor: The database cursor.
    :param project_id: The project id to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        -- selects all genesets for the given project ID
        SELECT geneset.*
        FROM production.geneset INNER JOIN production.project2geneset
        ON geneset.gs_id=project2geneset.gs_id
        WHERE project2geneset.pj_id=%(project_id)s
        """,
        {"project_id": project_id},
    )
    return cursor.fetchall()


def by_project_id_and_user_id(cursor: Cursor, project_id: int, user_id: int) -> List:
    """Get geneset info by project id.

    :param cursor: The database cursor.
    :param project_id: The project id to search for.
    :param user_id: The user id (internal) to limit results to.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        -- selects all genesets for the given project ID
        SELECT geneset.*
        FROM geneset INNER JOIN project2geneset
        ON geneset.gs_id=project2geneset.gs_id
        WHERE project2geneset.pj_id=%(project_id)s
            -- security check: make sure the authenticated user has the
            -- right to view the geneset
        AND geneset_is_readable2(%(user_id)s, geneset.gs_id);
        """,
        {"project_id": project_id, "user_id": user_id},
    )
    return cursor.fetchall()


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
    return result == 1 and type(result) is not bool


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
