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


def add_ontology_term_to_geneset(
    cursor: Cursor, ontology_term_id: int, geneset_id: int, gso_ref_type: str
) -> Optional[Row]:
    """Relate an ontology term with a geneset. Insert association.

    :param cursor: A database cursor
    :param ontology_term_id: ontology term id to associate with geneset
    :param geneset_id: geneset identifier to add to project
    :param gso_ref_type: geneset ontology reference type

    :return: record of created the association (geneset id, ontology_term_id)
    """
    cursor.execute(
        *ontology_query.insert_geneset_ontology_term_association(
            geneset_id=geneset_id,
            ontology_term_id=ontology_term_id,
            gso_ref_type=gso_ref_type,
        )
    )

    return cursor.fetchone()


def delete_ontology_term_from_geneset(
    cursor: Cursor, ontology_term_id: int, geneset_id: int, gso_ref_type: str
) -> Optional[Row]:
    """Remove ontology term from a geneset. Delete association.

    :param cursor: A database cursor
    :param ontology_term_id: ontology term id to delete from geneset
    :param geneset_id: geneset identifier to add to project
    :param gso_ref_type: geneset ontology reference type

    :return: record of deleted the association (geneset id, ontology_term_id)
    """
    cursor.execute(
        *ontology_query.delete_geneset_ontology_term_association(
            geneset_id=geneset_id,
            ontology_term_id=ontology_term_id,
            gso_ref_type=gso_ref_type,
        )
    )

    return cursor.fetchone()
