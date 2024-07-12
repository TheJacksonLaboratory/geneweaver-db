"""Database code for interacting with Publication table."""

from typing import Iterable, List, Optional

from geneweaver.core.schema.publication import PublicationInfo
from geneweaver.db.query import publication as publication_query
from psycopg import Cursor, rows
from psycopg.rows import Row


def by_pubmed_id(cursor: Cursor, pubmed_id: int) -> Optional[rows.Row]:
    """Get a publication by PubMed ID.

    :param cursor: The database cursor.
    :param pubmed_id: The PubMed ID to search for.

    :return: optional row using `.fetchone()`
    """
    cursor.execute(*publication_query.by_pubmed_id(pubmed_id))
    return cursor.fetchone()


def by_pubmed_ids(cursor: Cursor, pubmed_ids: Iterable[int]) -> List[rows.Row]:
    """Get publications by a list of PubMed IDs.

    :param cursor: The database cursor.
    :param pubmed_ids: The PubMed IDs to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(*publication_query.by_pubmed_ids(pubmed_ids))
    return cursor.fetchall()


def by_id(cursor: Cursor, pub_id: int) -> Optional[rows.Row]:
    """Get a publication by ID.

    :param cursor: The database cursor.
    :param pub_id: The publication ID (geneweaver internal) to search for.

    :return: optional row using `.fetchone()`
    """
    cursor.execute(*publication_query.by_id(pub_id))
    return cursor.fetchone()


def by_geneset_id(cursor: Cursor, geneset_id: int) -> Optional[rows.Row]:
    """Get a publication by geneset ID.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to search for.

    :return: optional row using `.fetchone()`
    """
    cursor.execute(*publication_query.by_geneset_id(geneset_id))
    return cursor.fetchone()


def add(cursor: Cursor, publication: PublicationInfo) -> Optional[rows.Row]:
    """Add a publication to the database.

    :param cursor: The database cursor.
    :param publication: The publication to add.

    :return: optional row using `.fetchone()`
    """
    cursor.execute(*publication_query.add(**publication.model_dump()))
    return cursor.fetchone()


def get(
    cursor: Cursor,
    pub_id: Optional[int] = None,
    authors: Optional[str] = None,
    title: Optional[str] = None,
    abstract: Optional[str] = None,
    journal: Optional[str] = None,
    volume: Optional[str] = None,
    pages: Optional[str] = None,
    month: Optional[str] = None,
    year: Optional[str] = None,
    pubmed: Optional[str] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get publications by some criteria.

    :param cursor: An async database cursor.
    :param pub_id: Show only results with this publication id
    :param authors: Show only results with these authors
    :param title: Show only results with this title
    :param abstract: Show only results with this abstract
    :param journal: Show only results with this journal
    :param volume: Show only results with volume
    :param pages: Show only results with these pages
    :param month: Show only results with this publication month
    :param year: Show only results with publication year
    :param pubmed: Show only results with pubmed id
    :param search_text: Show only results that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.

    """
    cursor.execute(
        *publication_query.get(
            pub_id=pub_id,
            authors=authors,
            title=title,
            abstract=abstract,
            journal=journal,
            volume=volume,
            pages=pages,
            month=month,
            year=year,
            pubmed=pubmed,
            search_text=search_text,
            limit=limit,
            offset=offset,
        )
    )

    return cursor.fetchall()
