"""Database code for interacting with Publication table."""
from typing import Iterable, List, Optional

from geneweaver.db.utils import format_sql_fields
from psycopg import Cursor, rows
from psycopg.sql import SQL

PUB_FIELD_MAP = {
    "pub_id": "id",
    "pub_authors": "authors",
    "pub_title": "title",
    "pub_abstract": "abstract",
    "pub_journal": "journal",
    "pub_volume": "volume",
    "pub_pages": "pages",
    "pub_month": "month",
    "pub_year": "year",
    "pub_pubmed": "pubmed_id",
}

PUB_FIELDS = format_sql_fields(PUB_FIELD_MAP, query_table="publication")

PUB_QUERY = SQL("SELECT") + SQL(",").join(PUB_FIELDS) + SQL("FROM publication")


def by_pubmed_id(cursor: Cursor, pubmed_id: str) -> Optional[rows.Row]:
    """Get a publication by PubMed ID.

    :param cursor: The database cursor.
    :param pubmed_id: The PubMed ID to search for.

    :return: optional row using `.fetchone()`
    """
    query = (PUB_QUERY + SQL("WHERE pub_pubmed = %(pmid)s")).join(" ")
    cursor.execute(query, {"pmid": pubmed_id})
    return cursor.fetchone()


def by_pubmed_ids(cursor: Cursor, pubmed_ids: Iterable[str]) -> List[rows.Row]:
    """Get publications by a list of PubMed IDs.

    :param cursor: The database cursor.
    :param pubmed_ids: The PubMed IDs to search for.

    :return: list of results using `.fetchall()`
    """
    query = (PUB_QUERY + SQL("WHERE pub_pubmed = ANY(%(pubmed_ids)s)")).join(" ")
    cursor.execute(query, {"pubmed_ids": list(pubmed_ids)})
    return cursor.fetchall()


def by_id(cursor: Cursor, pub_id: int) -> Optional[rows.Row]:
    """Get a publication by ID.

    :param cursor: The database cursor.
    :param pub_id: The publication ID (geneweaver internal) to search for.

    :return: optional row using `.fetchone()`
    """
    query = (PUB_QUERY + SQL("WHERE pub_id = %(pub_id)s")).join(" ")
    cursor.execute(query, {"pub_id": pub_id})
    return cursor.fetchone()


def by_geneset_id(cursor: Cursor, geneset_id: int) -> Optional[rows.Row]:
    """Get a publication by geneset ID.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to search for.

    :return: optional row using `.fetchone()`
    """
    query = (
        PUB_QUERY
        + SQL("JOIN geneset ON publication.pub_id = geneset.pub_id")
        + SQL("WHERE gs_id = %(geneset_id)s")
    ).join(" ")

    cursor.execute(query, {"geneset_id": geneset_id})
    return cursor.fetchone()
