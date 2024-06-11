"""Database code for interacting with Project table."""

from typing import List, Optional

from geneweaver.db.query import project as project_query
from psycopg import AsyncCursor
from psycopg.rows import Row


async def get(
    cursor: AsyncCursor,
    project_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    name: Optional[str] = None,
    starred: Optional[bool] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get projects from the database.

    :param cursor: A database asynch cursor.
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
    await cursor.execute(
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

    return await cursor.fetchall()
