"""Database code for interacting with Publication table."""

from typing import Iterable, List, Optional

from geneweaver.core.schema.publication import PublicationInfo
from geneweaver.db.query import publication as publication_query
from psycopg import Cursor, rows


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
    cursor.execute(*publication_query.add(**publication.dict()))
    return cursor.fetchone()
