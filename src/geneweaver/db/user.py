"""Functions for querying the user table.

These functions are used to query the user table in the database. They come in two
distinct "flavors": those that return one or more entire user record, and those
that return a single value from a user record. The functions that return one or
more entire user records will return to you the result of calling fetchall() or
fetchone() on the cursor. The functions that return a single value from a user
record will return to you a value extracted from the result of calling fetchone()
or fetchall() on the cursor.

The functions that return one or more entire user records are:
- by_api_key
- by_sso_id
- by_user_id
- by_email

The functions that return a single value from a user record are:
- user_id_from_api_key
- user_id_from_sso_id
"""
from typing import List, Optional

from psycopg import Cursor


def user_id_from_api_key(cursor: Cursor, api_key: str) -> Optional[int]:
    """Get user id from api key.

    :param cursor: The database cursor.
    :param api_key: The api key to search for.

    :return: The user id (internal) if found, otherwise None.
    """
    cursor.execute(
        """SELECT usr_id FROM production.usr WHERE apikey = %(api_key)s;""",
        {"api_key": api_key},
    )
    result = cursor.fetchone()
    return result[0] if result else None


def user_id_from_sso_id(cursor: Cursor, sso_id: str) -> Optional[int]:
    """Get user id from sso id.

    :param cursor: The database cursor.
    :param sso_id: The sso id to search for.

    :return: The user id (internal) if found, otherwise None.
    """
    cursor.execute(
        """SELECT usr_id FROM production.usr WHERE usr_sso_id = %(sso_id)s;""",
        {"sso_id": sso_id},
    )
    result = cursor.fetchone()
    return result[0] if result else None


def by_api_key(cursor: Cursor, api_key: str) -> List:
    """Get user info by api key.

    :param cursor: The database cursor.
    :param api_key: The api key to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT * FROM production.usr WHERE apikey = %(api_key)s;""",
        {"api_key": api_key},
    )
    return cursor.fetchall()


def by_sso_id(cursor: Cursor, sso_id: str) -> List:
    """Get user info by sso id.

    :param cursor: The database cursor.
    :param sso_id: The sso id to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT * FROM production.usr WHERE usr_sso_id = %(sso_id)s;""",
        {"sso_id": sso_id},
    )
    return cursor.fetchall()


def by_user_id(cursor: Cursor, user_id: int) -> List:
    """Get user info by user id.

    :param cursor: The database cursor.
    :param user_id: The user id (internal) to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT * FROM production.usr WHERE usr_id = %(user_id)s;""",
        {"user_id": user_id},
    )
    return cursor.fetchall()


def by_email(cursor: Cursor, email: str) -> List:
    """Get user info by email.

    :param cursor: The database cursor.
    :param email: The email to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """SELECT * FROM production.usr WHERE usr_email = %(email)s;""",
        {"email": email},
    )
    return cursor.fetchall()
