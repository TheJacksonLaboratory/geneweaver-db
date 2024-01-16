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

from geneweaver.db.utils import temp_override_row_factory
from psycopg import Cursor, rows


@temp_override_row_factory(rows.tuple_row)
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


@temp_override_row_factory(rows.tuple_row)
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


def by_sso_id_and_email(cursor: Cursor, sso_id: str, email: str) -> List:
    """Get user info by sso id and email.

    :param cursor: The database cursor.
    :param sso_id: The sso id to search for.
    :param email: The email to search for.

    :return: list of results using `.fetchall()`
    """
    cursor.execute(
        """
        SELECT * FROM production.usr
        WHERE usr_sso_id = %(sso_id)s AND usr_email = %(email)s;
        """,
        {"sso_id": sso_id, "email": email},
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


@temp_override_row_factory(rows.tuple_row)
def email_exists(cursor: Cursor, email: str) -> bool:
    """Check if email exists.

    :param cursor: The database cursor.
    :param email: The email to check.

    :return: True if the email exists, otherwise False.
    """
    cursor.execute(
        """ SELECT count(*) FROM usr
            WHERE usr_email = %s
        """,
        (email,),
    )
    existing = int(cursor.fetchone()[0])

    return existing > 0


@temp_override_row_factory(rows.tuple_row)
def sso_id_exists(cursor: Cursor, sso_id: str) -> bool:
    """Check if sso id exists.

    :param cursor: The database cursor.
    :param sso_id: The sso id to check.

    :return: True if the sso id exists, otherwise False.
    """
    cursor.execute(
        """ SELECT count(*) FROM usr
            WHERE usr_sso_id = %s
        """,
        (sso_id,),
    )
    existing = int(cursor.fetchone()[0])

    return existing > 0


@temp_override_row_factory(rows.tuple_row)
def link_user_id_with_sso_id(cursor: Cursor, user_id: int, sso_id: str) -> int:
    """Link a user id with an sso id.

    :param cursor: The database cursor.
    :param user_id: The user id (internal) to link.
    :param sso_id: The sso id to link.

    :return: The user id (internal) of the user that was linked.

    :raises ValueError: If the sso id is already linked to a different account.
    """
    if sso_id_exists(cursor, sso_id):
        raise ValueError("SSO ID is already linked to a different account")

    cursor.execute(
        """UPDATE usr
       SET usr_sso_id = %s
       WHERE usr_id = %s
       RETURNING usr_id;
       """,
        (sso_id, user_id),
    )
    cursor.connection.commit()
    return cursor.fetchone()[0]


@temp_override_row_factory(rows.tuple_row)
def create_sso_user(cursor: Cursor, name: str, email: str, sso_id: str) -> int:
    """Create a new user with sso id.

    :param cursor: The database cursor.
    :param name: The user's name.
    :param email: The user's email address.
    :param sso_id: The user's sso id.

    :return: The user id (internal) of the newly created user.
    """
    split_name = name.split(" ")
    first_name = split_name[0]
    last_name = " ".join(split_name[1:])

    cursor.execute(
        """INSERT INTO usr
           (usr_first_name, usr_last_name,
           usr_email, usr_admin, usr_sso_id,
           usr_last_seen, usr_created, is_guest)
           VALUES
           (%(user_first_name)s, %(user_last_name)s,
           %(user_email)s, '0', %(user_sso_id)s,
           NOW(), NOW(), 'f')
           RETURNING usr_id;
        """,
        {
            "user_first_name": first_name,
            "user_last_name": last_name,
            "user_email": email.lower(),
            "user_sso_id": sso_id,
        },
    )
    cursor.connection.commit()

    return cursor.fetchone()[0]
