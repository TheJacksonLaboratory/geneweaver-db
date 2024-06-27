"""Database health functions."""

from typing import List

from psycopg import Cursor
from psycopg.rows import Row
from psycopg.sql import SQL


def check_last_gi_update(
    cursor: Cursor,
) -> List[Row]:
    """Check last update for gene indentifier.

    :param cursor: db cursor
    """
    query = SQL("SELECT gi_date FROM gene_info ORDER BY gi_date DESC LIMIT 1")
    cursor.execute(query)

    return cursor.fetchone()


def check_geneset_count(
    cursor: Cursor,
) -> List[Row]:
    """Check geneset record count.

    :param cursor: db cursor
    """
    query = SQL("SELECT count(*) FROM geneset")
    cursor.execute(query)

    return cursor.fetchone()


def check_gene_count(
    cursor: Cursor,
) -> List[Row]:
    """Check gene record count.

    :param cursor: db cursor
    """
    query = SQL("SELECT count(*) FROM genedb")
    cursor.execute(query)

    return cursor.fetchone()


def health_check(
    cursor: Cursor,
) -> dict:
    """Check DB health.

    :param cursor: db cursor
    """
    health_reponse = {}

    # gene identifier last update
    gi_update = check_last_gi_update(cursor=cursor)
    health_reponse["gene_identifier_last_update"] = gi_update

    # gene count
    gene_count = check_gene_count(cursor=cursor)
    health_reponse["gene_count"] = gene_count

    # geneset count
    geneset_count = check_geneset_count(cursor=cursor)
    health_reponse["geneset_count"] = geneset_count

    return health_reponse
