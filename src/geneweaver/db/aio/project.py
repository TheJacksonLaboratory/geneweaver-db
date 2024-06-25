"""Database code for interacting with Project table."""

from typing import List, Optional

from geneweaver.core.schema.project import ProjectCreate
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

    :param cursor: A database async cursor.
    :param project_id: Show only results for this project identifier id
    :param owner_id: Show only results owned by this user ID.
    :param name: Show only results with this project name
    :param starred: Show projects with star flag
    :param search_text: Return projects that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :return: list of results using `.fetchall()`
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


async def shared_with_user(
    cursor: AsyncCursor,
    user_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Row]:
    """Get projects shared with the given user id.

    :param cursor: A database async cursor.
    :param user_id: Show only results with projects shared with this user id
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :return: list of results using `.fetchall()`
    """
    await cursor.execute(
        *project_query.shared_with_user(user_id=user_id, limit=limit, offset=offset)
    )

    return await cursor.fetchall()


async def add(
    cursor: AsyncCursor, project: ProjectCreate, user_id: int, starred: bool = False
) -> Optional[Row]:
    """Add a new project.

    :param cursor: A database async cursor
    :param project: project data for creation
    :param user_id: user id to insert
    :param starred: start indicator

    :return: The ID of the added project
    """
    await cursor.execute(
        *project_query.add(user_id=user_id, starred=starred, **project.dict())
    )

    return await cursor.fetchone()


async def add_geneset_to_project(
    cursor: AsyncCursor, project_id: int, geneset_id: int
) -> Optional[Row]:
    """Add a genset to a project. Insert association.

    :param cursor: An async database cursor
    :param project_id: project identifier id to associate with geneset
    :param geneset_id: geneset identifier to add to project

    :return: record of the association
    """
    await cursor.execute(
        *project_query.insert_geneset_to_project(
            project_id=project_id, geneset_id=geneset_id
        )
    )

    return await cursor.fetchone()


async def delete_geneset_from_project(
    cursor: AsyncCursor, project_id: int, geneset_id: int
) -> Optional[Row]:
    """Delete a genset from a project. Remove association.

    :param cursor: An async database cursor
    :param project_id: project identifier id to remove association with geneset
    :param geneset_id: geneset identifier to remove from project

    :return:
    """
    await cursor.execute(
        *project_query.remove_geneset_from_project(
            project_id=project_id, geneset_id=geneset_id
        )
    )

    return await cursor.fetchone()
