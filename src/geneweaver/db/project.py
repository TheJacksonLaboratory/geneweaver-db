"""Database code for interacting with Project table."""

from typing import List, Optional

from geneweaver.db.query import project as project_query
from psycopg import Cursor
from psycopg.rows import Row


def get(
    cursor: Cursor,
    project_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    name: Optional[str] = None,
    starred: Optional[bool] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get projects from the database.

    :param cursor: A database cursor.
    :param project_id: Show only results for this project identifier id
    :param owner_id: Show only results owned by this user ID.
    :param name: Show only results with this project name
    :param starred: Show projects with star flag
    :param search_text: Return projects that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    @return:
    """
    cursor.execute(
        *project_query.get(
            project_id=project_id,
            owner_id=owner_id,
            name=name,
            starred=starred,
            search_text=search_text,
            limit=limit,
            offset=offset,
        )
    )

    return cursor.fetchall()


def shared_with_user(
    cursor: Cursor,
    user_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get projects shared with the given user id.

    :param cursor: A database cursor.
    :param user_id: Show only results with projects shared with this user id
    :param limit: Limit the number of results.
    :param offset: Offset the results.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        *project_query.shared_with_user(user_id=user_id, limit=limit, offset=offset)
    )

    return cursor.fetchall()
