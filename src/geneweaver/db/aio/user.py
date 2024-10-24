"""Functions for querying the user table.

The functions that return one or more entire user records are:
- by_api_key
- by_sso_id
- by_user_id
- by_email
"""

from typing import Optional

from geneweaver.core.schema.user import User
from geneweaver.db.query import user
from geneweaver.db.utils import temp_override_row_factory
from psycopg import AsyncCursor, rows


async def __fetch_and_return_user(cursor: AsyncCursor) -> Optional[User]:
    """Fetch and return a user from the cursor.

    :param cursor: The database cursor.

    :return: The user if found, otherwise None.
    """
    result = await cursor.fetchone()
    return User(**result) if result else None


async def by_api_key(cursor: AsyncCursor, api_key: str) -> Optional[User]:
    """Get user info by api key.

    :param cursor: The database cursor.
    :param api_key: The api key to search for.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(*user.by_api_key(api_key))
    return await __fetch_and_return_user(cursor)


async def by_sso_id(cursor: AsyncCursor, sso_id: str) -> Optional[User]:
    """Get user info by sso id.

    :param cursor: The database cursor.
    :param sso_id: The sso id to search for.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(*user.by_sso_id(sso_id))
    return await __fetch_and_return_user(cursor)


async def by_sso_id_and_email(
    cursor: AsyncCursor, sso_id: str, email: str
) -> Optional[User]:
    """Get user info by sso id and email.

    :param cursor: The database cursor.
    :param sso_id: The sso id to search for.
    :param email: The email to search for.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(*user.by_sso_id_and_email(sso_id, email))
    return await __fetch_and_return_user(cursor)


async def by_user_id(cursor: AsyncCursor, user_id: int) -> Optional[User]:
    """Get user info by user id.

    :param cursor: The database cursor.
    :param user_id: The user id (internal) to search for.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(*user.by_id(user_id))
    return await __fetch_and_return_user(cursor)


async def by_email(cursor: AsyncCursor, email: str) -> Optional[User]:
    """Get user info by email.

    :param cursor: The database cursor.
    :param email: The email to search for.

    :return: list of results using `.fetchall()`
    """
    await cursor.execute(*user.by_email(email))
    return await __fetch_and_return_user(cursor)


@temp_override_row_factory(rows.tuple_row)
async def email_exists(cursor: AsyncCursor, email: str) -> bool:
    """Check if email exists.

    :param cursor: The database cursor.
    :param email: The email to check.

    :return: True if the email exists, otherwise False.
    """
    await cursor.execute(*user.email_exists(email))
    exists = bool((await cursor.fetchone())[0])
    return exists


@temp_override_row_factory(rows.tuple_row)
async def sso_id_exists(cursor: AsyncCursor, sso_id: str) -> bool:
    """Check if sso id exists.

    :param cursor: The database cursor.
    :param sso_id: The sso id to check.

    :return: True if the sso id exists, otherwise False.
    """
    await cursor.execute(*user.sso_id_exists(sso_id))
    exists = bool((await cursor.fetchone())[0])
    return exists


@temp_override_row_factory(rows.tuple_row)
async def is_curator_or_higher(cursor: AsyncCursor, user_id: int) -> bool:
    """Check if a user is a curator or higher.

    :param cursor: The database cursor.
    :param user_id: The user id to check.

    :return: True if the user is a curator or higher, otherwise False.
    """
    await cursor.execute(*user.is_curator_or_higher(user_id))
    exists = bool((await cursor.fetchone())[0])
    return exists


@temp_override_row_factory(rows.tuple_row)
async def is_assigned_curation(
    cursor: AsyncCursor, user_id: int, geneset_id: int
) -> bool:
    """Check if a user is assigned curation.

    :param cursor: The database cursor.
    :param user_id: The user id to check.
    :param geneset_id: The geneset id to check.

    :return: True if the user is assigned curation, otherwise False.
    """
    await cursor.execute(*user.is_assigned_curation(user_id, geneset_id))
    exists = bool((await cursor.fetchone())[0])
    return exists
