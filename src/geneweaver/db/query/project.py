"""Query generation functions for projects."""

from typing import Optional, Tuple

from geneweaver.db.query.utils import construct_filters, search
from geneweaver.db.utils import format_sql_fields, limit_and_offset
from psycopg.sql import SQL, Composed, Identifier

PROJECT_TSVECTOR = (Identifier("project") + Identifier("pj_tsvector")).join(".")

PROJECT_FIELD_MAP = {
    "pj_id": "id",
    "usr_id": "owner_id",
    "pj_name": "name",
    "pj_groups": "groups",
    "pj_notes": "notes",
    "pj_created": "created",
    "pj_star": "star",
}
PROJECT_FIELDS = format_sql_fields(PROJECT_FIELD_MAP, query_table="project")


def get(
    project_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    name: Optional[str] = None,
    starred: Optional[bool] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[Composed, dict]:
    """Get projects by any filtering criteria.

    :param project_id: Show only results for this project identifier id
    :param owner_id: Show only results owned by this user ID.
    :param name: Show only results with this project name
    :param starred: Show projects with star flag
    :param search_text: Return projects that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.

    :return: A query (and params) that can be executed on a cursor.
    """
    params = {}
    filtering = []
    query = SQL("SELECT")
    query = query + SQL(",").join(PROJECT_FIELDS) + SQL("FROM project")

    filtering, params = search(PROJECT_TSVECTOR, filtering, params, search_text)

    filtering, params = construct_filters(
        filtering,
        params,
        {"id": project_id, "usr_id": owner_id, "name": name, "star": starred},
    )

    if len(filtering) > 0:
        query += SQL("WHERE") + SQL("AND").join(filtering)

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params


def shared_with_user(
    user_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[Composed, dict]:
    """Get projects shared with the given user id.

    :param user_id: Show only results with projects shared with this user id
    :param limit: Limit the number of results.
    :param offset: Offset the results.

    :return: A query (and params) that can be executed on a cursor.
    """
    query_fields = (
        SQL("COUNT(gs_id),")
        + SQL(",").join(PROJECT_FIELDS)
        + SQL(",usr_email AS owner")
    )
    query = SQL("SELECT")
    query = (
        query
        + query_fields
        + SQL("FROM project")
        + SQL("NATURAL JOIN project2geneset, usr")
        + SQL("WHERE usr.usr_id=project.usr_id")
        + SQL("AND project.usr_id<>%(user_id)s")
        + SQL("AND project_is_readable(%(user_id)s, pj_id)")
        + SQL("GROUP BY project.usr_id, pj_name, pj_id, owner")
        + SQL("ORDER BY pj_name")
    ).join(" ")
    params = {"user_id": user_id}

    query = limit_and_offset(query, limit, offset).join("")
    return query, params


def add(
    user_id: int,
    name: str,
    notes: str,
    starred: bool = False,
) -> Tuple[Composed, dict]:
    """Add a new project.

    :param user_id: user id to insert
    :param name: project name to insert
    :param notes: project notes to insert
    :param starred: start indicator

    :return: A query (and params) that can be executed on a cursor.
    """
    start_char = "t" if starred else "f"
    params = {"user_id": user_id, "name": name, "notes": notes, "star": start_char}

    values = "VALUES (%(name)s, %(user_id)s, %(notes)s, %(star)s, now())"
    query = (
        SQL("INSERT INTO project (pj_name, usr_id, pj_notes, pj_star, pj_created)")
        + SQL(values)
        + SQL("RETURNING pj_id")
    ).join(" ")

    return query, params


def insert_geneset_to_project(
    project_id: int, geneset_id: int
) -> Tuple[Composed, dict]:
    """Add a genset to a project. Insert association.

    :param project_id: project identifier id to associate with geneset
    :param geneset_id: geneset identifier to add to project

    :return: A query (and params) that can be executed on a cursor.
    """
    params = {"project_id": project_id, "geneset_id": geneset_id}
    values = "VALUES (%(project_id)s, %(geneset_id)s, now())"
    query = (
        SQL("INSERT INTO project2geneset (pj_id, gs_id, modified_on)")
        + SQL(values)
        + SQL("RETURNING pj_id, gs_id")
    ).join(" ")

    return query, params


def remove_geneset_from_project(
    project_id: int, geneset_id: int
) -> Tuple[Composed, dict]:
    """Delete a genset from a project. Remove association.

    :param project_id: project identifier id to associate with geneset
    :param geneset_id: geneset identifier to add to project

    :return: A query (and params) that can be executed on a cursor.
    """
    params = {"project_id": project_id, "geneset_id": geneset_id}
    query = (
        SQL("DELETE FROM project2geneset")
        + SQL("WHERE pj_id = %(project_id)s AND gs_id = %(geneset_id)s")
        + SQL("RETURNING pj_id, gs_id")
    ).join(" ")

    return query, params
