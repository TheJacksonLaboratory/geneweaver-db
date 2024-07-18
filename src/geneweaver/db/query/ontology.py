"""Query generation functions for ontologies."""

from typing import Optional, Tuple

from geneweaver.db.utils import limit_and_offset
from psycopg.sql import SQL, Composed


def by_geneset(
    geneset_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[Composed, dict]:
    """Create a psycopg query to get genesets ontologies.

    :param geneset_id: The geneset identifier to search for.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = SQL("SELECT")
    query_fields = (
        SQL("geneset.gs_id AS geneset_id")
        + SQL(",ontology.ont_ref_id AS ontology_term_id")
        + SQL(",ontology.ont_name AS name")
        + SQL(",ontology.ont_description as description")
        + SQL(",ontologydb.ontdb_name as source_ontology")
    )
    query = (
        query
        + query_fields
        + SQL("FROM geneset")
        + SQL("JOIN geneset_ontology ON geneset.gs_id = geneset_ontology.gs_id")
        + SQL("JOIN ontology ON geneset_ontology.ont_id = ontology.ont_id")
        + SQL("JOIN ontologydb ON ontology.ontdb_id = ontologydb.ontdb_id")
        + SQL("WHERE geneset.gs_id = %(gs_id)s")
    ).join(" ")
    params = {"gs_id": geneset_id}

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params


def insert_geneset_ontology_term_association(
    ontology_term_id: int, geneset_id: int, gso_ref_type: str
) -> Tuple[Composed, dict]:
    """Relate an ontology term with a geneset. Insert association.

    :param ontology_term_id: ontology term id to associate with geneset
    :param geneset_id: geneset identifier
    :param gso_ref_type: geneset ontology reference type

    :return: A query (and params) that can be executed on a cursor.
    """
    params = {
        "geneset_id": geneset_id,
        "ontology_term_id": ontology_term_id,
        "gso_ref_type": gso_ref_type,
    }
    values = "VALUES (%(geneset_id)s, %(ontology_term_id)s, %(gso_ref_type)s)"
    query = (
        SQL("INSERT INTO geneset_ontology (gs_id, ont_id, gso_ref_type)")
        + SQL(values)
        + SQL("RETURNING gs_id, ont_id")
    ).join(" ")

    return query, params


def delete_geneset_ontology_term_association(
    ontology_term_id: int, geneset_id: int, gso_ref_type: str
) -> Tuple[Composed, dict]:
    """Remove an ontology term from a geneset. Delete association.

    :param ontology_term_id: ontology term id to delete from geneset
    :param geneset_id: geneset identifier
    :param gso_ref_type: geneset ontology reference type

    :return: A query (and params) that can be executed on a cursor.
    """
    params = {
        "geneset_id": geneset_id,
        "ontology_term_id": ontology_term_id,
        "gso_ref_type": gso_ref_type,
    }

    query = (
        SQL("DELETE FROM geneset_ontology")
        + SQL("WHERE gs_id = %(geneset_id)s ")
        + SQL("AND ont_id=%(ontology_term_id)s")
        + SQL("AND gso_ref_type=%(gso_ref_type)s")
        + SQL("RETURNING gs_id, ont_id")
    ).join(" ")

    return query, params


def by_ontology_db(
    ontology_db_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[Composed, dict]:
    """Create a psycopg query to get ontology terms by ontology id.

    :param ontology_db_id: The ontology DB identifier to search for.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = SQL("SELECT")
    query_fields = (
        SQL("ontology.ont_ref_id AS ontology_term_id")
        + SQL(",ontology.ont_name AS name")
        + SQL(",ontology.ont_description as description")
        + SQL(",ontologydb.ontdb_name as source_ontology")
    )
    query = (
        query
        + query_fields
        + SQL("FROM ontology")
        + SQL("JOIN ontologydb ON ontology.ontdb_id = ontologydb.ontdb_id")
        + SQL("WHERE ontology.ontdb_id = %(ontology_db_id)s")
    ).join(" ")
    params = {"ontology_db_id": ontology_db_id}

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params


def get_ontology_dbs(
    ontology_db_id: Optional[int] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[Composed, dict]:
    """Create a psycopg query to get ontology terms by ontology id.

    :param ontology_db_id: The ontology DB identifier to search for.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.

    :return: A query (and params) that can be executed on a cursor.
    """
    query = SQL("SELECT")
    query_fields = (
        SQL("onto_db.ontdb_id AS ontology_db_id")
        + SQL(",onto_db.ontdb_name AS name")
        + SQL(",onto_db.ontdb_prefix as prefix")
        + SQL(",onto_db.ontdb_linkout_url as url")
    )
    query = (query + query_fields + SQL("FROM ontologydb as onto_db")).join(" ")

    params = {}
    if ontology_db_id is not None:
        query = (query + SQL("WHERE onto_db.ontdb_id = %(ontology_db_id)s")).join(" ")
        params["ontology_db_id"] = ontology_db_id

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params


def by_ontology_term(onto_ref_term_id: str) -> Tuple[Composed, dict]:
    """Create a psycopg query to get ontology term by ontology reference id.

    :param onto_ref_term_id: The ontology term reference identifier to search for.
    :return: A query (and params) that can be executed on a cursor.
    """
    query = SQL("SELECT")
    query_fields = (
        SQL("ontology.ont_id AS onto_id")
        + SQL(",ontology.ont_ref_id AS onto_ref_term_id")
        + SQL(",ontology.ont_name AS name")
        + SQL(",ontology.ont_description as description")
        + SQL(",ontologydb.ontdb_name as source_ontology")
    )
    query = (
        query
        + query_fields
        + SQL("FROM ontology")
        + SQL("JOIN ontologydb ON ontology.ontdb_id = ontologydb.ontdb_id")
        + SQL("WHERE ontology.ont_ref_id = %(onto_ref_term_id)s")
    ).join(" ")
    params = {"onto_ref_term_id": onto_ref_term_id}

    return query, params
