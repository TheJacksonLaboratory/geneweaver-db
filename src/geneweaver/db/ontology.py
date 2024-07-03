"""Database code for interacting with ontologies."""

from typing import List, Optional

from geneweaver.db.query import ontology as ontology_query
from psycopg import Cursor
from psycopg.rows import Row


def by_geneset(
    cursor: Cursor,
    geneset_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get geneset ontologies from the database.

    :param cursor: A database cursor.
    :param geneset_id: Show only results for this geneset identifier
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    @return:
    """
    cursor.execute(
        *ontology_query.by_geneset(
            geneset_id=geneset_id,
            limit=limit,
            offset=offset,
        )
    )

    return cursor.fetchall()
