"""Utilities for testing the database module."""
# ruff: noqa: ANN101, D102, D107
from unittest.mock import MagicMock

from psycopg import Cursor


def get_magic_mock_cursor(fetch_result) -> MagicMock:
    """Return a mock cursor with the given fetch result."""
    cursor = MagicMock(spec=Cursor)
    cursor.fetchone.return_value = fetch_result
    cursor.fetchall.return_value = fetch_result
    return cursor
