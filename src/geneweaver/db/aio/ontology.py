"""Database code for interacting with ontologies."""

from typing import List, Optional

from geneweaver.db.query import ontology as ontology_query
from psycopg import AsyncCursor
from psycopg.rows import Row


async def by_geneset(
    cursor: AsyncCursor,
    geneset_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get geneset ontologies from the database.

    :param cursor: An async database cursor.
    :param geneset_id: Show only results for this geneset identifier
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    @return:
    """
    await cursor.execute(
        *ontology_query.by_geneset(
            geneset_id=geneset_id,
            limit=limit,
            offset=offset,
        )
    )

    return await cursor.fetchall()


async def add_ontology_term_to_geneset(
    cursor: AsyncCursor, ontolog_term_id: int, geneset_id: int, gso_ref_type: str
) -> Optional[Row]:
    """Relate an ontology term with a geneset. Insert association.

    :param cursor: A async database cursor
    :param ontolog_term_id: ontology term id to associate with geneset
    :param geneset_id: geneset identifier to add to project
    :param gso_ref_type: geneset ontology reference type

    :return: record of created the association (geneset id, ontology_term_id)
    """
    await cursor.execute(
        *ontology_query.insert_geneset_ontology_term_association(
            geneset_id=geneset_id,
            ontology_term_id=ontolog_term_id,
            gso_ref_type=gso_ref_type,
        )
    )

    return await cursor.fetchone()
