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
        + SQL(",ontology.ont_ref_id AS ontology_id")
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
