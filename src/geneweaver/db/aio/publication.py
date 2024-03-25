"""Database code for interacting with Publication table."""

from typing import Iterable, List, Optional

from geneweaver.core.schema.publication import PublicationInfo
from geneweaver.db.query import publication as publication_query
from psycopg import AsyncCursor, rows


async def by_pubmed_id(cursor: AsyncCursor, pubmed_id: int) -> Optional[rows.Row]:
    """Get a publication by PubMed ID.

    :param cursor: The database cursor.
    :param pubmed_id: The PubMed ID to search for.

    :return: optional row using `.fetchone()`
    """
    await cursor.execute(*publication_query.by_pubmed_id(pubmed_id))
    return await cursor.fetchone()


async def by_pubmed_ids(
    cursor: AsyncCursor, pubmed_ids: Iterable[int]
) -> List[rows.Row]:
    """Get publications by a list of PubMed IDs.

    :param cursor: The database cursor.
    :param pubmed_ids: The PubMed IDs to search for.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(*publication_query.by_pubmed_ids(pubmed_ids))
    return await cursor.fetchall()


async def by_id(cursor: AsyncCursor, pub_id: int) -> Optional[rows.Row]:
    """Get a publication by ID.

    :param cursor: The database cursor.
    :param pub_id: The publication ID (geneweaver internal) to search for.

    :return: optional row using `.fetchone()`
    """
    await cursor.execute(*publication_query.by_id(pub_id))
    return await cursor.fetchone()


async def by_geneset_id(cursor: AsyncCursor, geneset_id: int) -> Optional[rows.Row]:
    """Get a publication by geneset ID.

    :param cursor: The database cursor.
    :param geneset_id: The geneset ID to search for.

    :return: optional row using `.fetchone()`
    """
    await cursor.execute(*publication_query.by_geneset_id(geneset_id))
    return await cursor.fetchone()


async def add(cursor: AsyncCursor, publication: PublicationInfo) -> Optional[rows.Row]:
    """Add a publication to the database.

    :param cursor: The database cursor.
    :param publication: The publication to add.

    :return: optional row using `.fetchone()`
    """
    await cursor.execute(*publication_query.add(**publication.dict()))
    return await cursor.fetchone()
