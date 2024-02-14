"""Database interaction code relating to Gene IDs."""
from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.query import gene as gene_query
from psycopg import AsyncCursor, rows


async def get(
    cursor: AsyncCursor,
    reference_id: Optional[str] = None,
    gene_database: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
    preferred: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List:
    """Get genes from the database.

    :param cursor: An async database cursor.
    :param reference_id: The reference id to search for.
    :param gene_database: The gene database to search for.
    :param species: The species to search for.
    :param preferred: Whether to search for preferred genes.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(
        *gene_query.get(
            reference_id=reference_id,
            gene_database=gene_database,
            species=species,
            preferred=preferred,
            limit=limit,
            offset=offset,
        )
    )

    return await cursor.fetchall()


async def get_preferred(
    cursor: AsyncCursor,
    gene_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[rows.Row]:
    """Get the preferred gene from the database for a given ode_id.

    :param cursor: An async database cursor.
    :param gene_id: The id of the gene to get.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.

    :return: The preferred gene using `.fetchone()`
    """
    await cursor.execute(
        *gene_query.get(
            gene_id=gene_id,
            preferred=True,
            limit=limit,
            offset=offset,
        )
    )

    return await cursor.fetchone()
