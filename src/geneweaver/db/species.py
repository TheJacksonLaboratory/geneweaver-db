"""Species database functions."""
from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.query.species import get
from psycopg import Cursor, rows


def get(
    cursor: Cursor,
    taxonomic_id: Optional[int] = None,
    reference_gene_db_id: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
) -> List:
    """Get species info.

    :param cursor: The database cursor.
    :param taxonomic_id: The taxonomic id.
    :param reference_gene_db_id: The reference gene database id.
    :param species: The species id.

    :return: All species that match the queries.
    """
    cursor.execute(
        *get(
            taxonomic_id=taxonomic_id,
            reference_gene_db_id=reference_gene_db_id,
            species=species,
        )
    )

    return cursor.fetchall()


def get_by_id(
    cursor: Cursor,
    species: Species,
) -> Optional[rows.Row]:
    """Get species info by species id.

    :param cursor: The database cursor.
    :param species: The species enum to query info for.
    :return: The species info for the provided enum.
    """
    cursor.execute(*get(species=species))

    return cursor.fetchone()
