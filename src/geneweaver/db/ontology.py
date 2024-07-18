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


def by_ontology_db(
    cursor: Cursor,
    ontology_db_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get ontology terms by ontology DB id from the database.

    :param cursor: An database cursor.
    :param ontology_db_id: Show only results for this ontology db identifier
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        *ontology_query.by_ontology_db(
            ontology_db_id=ontology_db_id,
            limit=limit,
            offset=offset,
        )
    )

    return cursor.fetchall()


def get_ontology_dbs(
    cursor: Cursor,
    ontology_db_id: Optional[int] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get available ontologies from the database.

    :param cursor: A database cursor.
    :param ontology_db_id: Show only results for this ontology db identifier
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        *ontology_query.get_ontology_dbs(
            ontology_db_id=ontology_db_id,
            limit=limit,
            offset=offset,
        )
    )

    return cursor.fetchall()


def by_ontology_term(cursor: Cursor, onto_ref_term_id: str) -> List[Row]:
    """Get ontology term by term ref id from the database.

    :param cursor: An database cursor.
    :param onto_ref_term_id: The ontology term reference identifier to search for.
    :return: ontology term record `.fetchone()`
    """
    cursor.execute(
        *ontology_query.by_ontology_term(
            onto_ref_term_id=onto_ref_term_id,
        )
    )

    return cursor.fetchone()
