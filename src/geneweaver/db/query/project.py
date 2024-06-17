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
    """Get project that are shared with a user.

    NOTE: NOT IMPLEMENTED
    """
    raise NotImplementedError()


def add(
    user_id: int,
    name: str,
    notes: str,
    starred: bool = False,
) -> Tuple[Composed, dict]:
    """Add a new publication.

    NOTE: NOT IMPLEMENTED
    """
    raise NotImplementedError()
