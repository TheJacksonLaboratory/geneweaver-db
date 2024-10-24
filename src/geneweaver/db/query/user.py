"""Query Builder for Users DB functions."""

from typing import Tuple

from geneweaver.db.utils import format_sql_fields
from psycopg.sql import SQL, Composed

USER_FIELD_MAP = {
    "usr_id": "id",
    "usr_email": "email",
    "usr_prefs": "prefs",
    "is_guest": "is_guest",
    "usr_first_name": "first_name",
    "usr_last_name": "last_name",
    "usr_admin": "admin",
    "usr_last_seen": "last_seen",
    "usr_created": "created",
    "ip_addr": "ip_address",
    "apikey": "api_key",
    "usr_sso_id": "sso_id",
}

USER_FIELDS = format_sql_fields(USER_FIELD_MAP, query_table="usr")


USER_QUERY = SQL("SELECT") + SQL(",").join(USER_FIELDS) + SQL("FROM usr")


def by_id(user_id: int) -> Tuple[Composed, dict]:
    """Get user by id."""
    query = USER_QUERY + SQL("WHERE usr_id = %(user_id)s;")
    params = {"user_id": user_id}
    return query.join(" "), params


def by_sso_id(sso_id: str) -> Tuple[Composed, dict]:
    """Get user by sso id."""
    query = USER_QUERY + SQL("WHERE usr_sso_id = %(user_id)s;")
    params = {"sso_id": sso_id}
    return query.join(" "), params


def by_email(email: str) -> Tuple[Composed, dict]:
    """Get user by email."""
    query = USER_QUERY + SQL("WHERE usr_email = %(email)s;")
    params = {"email": email}
    return query.join(" "), params


def by_sso_id_and_email(sso_id: str, email: str) -> Tuple[Composed, dict]:
    """Get user by sso id and email."""
    query = USER_QUERY + SQL("WHERE usr_sso_id = %(sso_id)s AND usr_email = %(email)s;")
    params = {"sso_id": sso_id, "email": email}
    return query.join(" "), params


def by_api_key(api_key: str) -> Tuple[Composed, dict]:
    """Get user by api key."""
    query = USER_QUERY + SQL("WHERE apikey = %(api_key)s;")
    params = {"api_key": api_key}
    return query.join(" "), params


def email_exists(email: str) -> Tuple[Composed, dict]:
    """Check if email exists."""
    query = SQL("SELECT") + SQL(
        "EXISTS(SELECT 1 FROM usr WHERE usr_email = %(email)s);"
    )
    params = {"email": email}
    return query.join(" "), params


def sso_id_exists(sso_id: str) -> Tuple[Composed, dict]:
    """Check if sso id exists."""
    query = SQL("SELECT") + SQL(
        "EXISTS(SELECT 1 FROM usr WHERE usr_sso_id = %(sso_id)s);"
    )
    params = {"sso_id": sso_id}
    return query.join(" "), params


def is_curator_or_higher__query() -> Composed:
    """Build SQL query to check if user is a curator or higher."""
    return (
        SQL("EXISTS(")
        + SQL("SELECT 1")
        + SQL("FROM usr")
        + SQL("WHERE usr_id = %(user_id)s")
        + SQL("AND usr_admin > 0)")
    )


def is_assigned_curation__query() -> Composed:
    """Build SQL query to check if user is assigned curation."""
    return (
        SQL("EXISTS(")
        + SQL("SELECT 1")
        + SQL("FROM curation_assignments")
        + SQL("WHERE curator = %(user_id)s")
        + SQL("AND gs_id = %(geneset_id)s")
        + SQL("AND curation_state = 2)")
    )


def is_curator_or_higher(user_id: int) -> Tuple[Composed, dict]:
    """Check if user is a curator or higher."""
    query = SQL("SELECT") + is_curator_or_higher__query() + SQL(";")
    params = {"user_id": user_id}
    return query.join(" "), params


def is_assigned_curation(user_id: int, geneset_id: int) -> Tuple[Composed, dict]:
    """Check if user is assigned curation."""
    query = SQL("SELECT") + is_assigned_curation__query() + SQL(";")
    params = {"user_id": user_id, "geneset_id": geneset_id}
    return query.join(" "), params
