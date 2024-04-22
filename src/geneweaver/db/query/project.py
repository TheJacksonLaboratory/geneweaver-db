"""Query generation functions for projects."""

from typing import Optional, Tuple

from psycopg.sql import Composed


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

    NOTE: NOT IMPLEMENTED
    """
    raise NotImplementedError()


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
