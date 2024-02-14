"""Generate SQL queries for publications."""
from typing import Iterable, Optional, Tuple

from geneweaver.db.utils import format_sql_fields
from psycopg import rows
from psycopg.sql import SQL, Composed

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


def by_id(pub_id: int) -> Optional[rows.Row]:
    """Create a psycopg query to get a publication by ID.

    :param pub_id: The publication ID (geneweaver internal) to search for.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = (PUB_QUERY + SQL("WHERE pub_id = %(pub_id)s")).join(" ")
    params = {"pub_id": pub_id}
    return query, params


def by_geneset_id(geneset_id: int) -> Tuple[Composed, dict]:
    """Create a psycopg query to get a publication by geneset ID.

    :param geneset_id: The geneset ID to search for.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = (
        PUB_QUERY
        + SQL("JOIN geneset ON publication.pub_id = geneset.pub_id")
        + SQL("WHERE gs_id = %(geneset_id)s")
    ).join(" ")

    params = {"geneset_id": geneset_id}
    return query, params


def by_pubmed_id(pubmed_id: str) -> Tuple[Composed, dict]:
    """Create a psycopg query to get a publication by PubMed ID.

    :param pubmed_id: The PubMed ID to search for.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = (PUB_QUERY + SQL("WHERE pub_pubmed = %(pmid)s")).join(" ")
    params = {"pmid": pubmed_id}
    return query, params


def by_pubmed_ids(pubmed_ids: Iterable[str]) -> Tuple[Composed, dict]:
    """Create a psycopg query to get publications by a list of PubMed IDs.

    :param pubmed_ids: The PubMed IDs to search for.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = (PUB_QUERY + SQL("WHERE pub_pubmed = ANY(%(pubmed_ids)s)")).join(" ")
    params = {"pubmed_ids": list(pubmed_ids)}
    return query, params
