"""Species database functions."""

from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.query import species as species_query
from psycopg import AsyncCursor, rows


async def get(
    cursor: AsyncCursor,
    taxonomic_id: Optional[int] = None,
    reference_gene_db_id: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
) -> List:
    """Get species info.

    :param cursor: An async database cursor.
    :param taxonomic_id: The taxonomic id.
    :param reference_gene_db_id: The reference gene database id.
    :param species: The species id.

    :return: All species that match the queries.
    """
    await cursor.execute(
        *species_query.get(
            taxonomic_id=taxonomic_id,
            reference_gene_db_id=reference_gene_db_id,
            species=species,
        )
    )

    return await cursor.fetchall()


async def get_by_id(
    cursor: AsyncCursor,
    species: Species,
) -> Optional[rows.Row]:
    """Get species info by species id.

    :param cursor: An async database cursor.
    :param species: The species enum to query info for.
    :return: The species info for the provided enum.
    """
    await cursor.execute(*species_query.get(species=species))

    return await cursor.fetchone()
