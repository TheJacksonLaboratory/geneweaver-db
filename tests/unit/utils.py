"""Utilities for testing the database module."""
# ruff: noqa: ANN101, D102, D107
from psycopg import sql as psql
from unittest.mock import MagicMock
from psycopg import Cursor


class MockCursor:
    """A mock database cursor to be used in place of a real cursor."""

    def __init__(self, fetch_result) -> None:
        self.fetch_result = fetch_result
        self.sql = None
        self.params = None

    def execute(self, sql, params):
        self.sql = sql
        self.params = params

    def fetchone(self):
        return self.fetch_result

    def fetchall(self):
        return self.fetch_result


def get_magic_mock_cursor(fetch_result) -> MagicMock:
    """Return a mock cursor with the given fetch result."""
    cursor = MagicMock(spec=Cursor)
    cursor.fetchone.return_value = fetch_result
    cursor.fetchall.return_value = fetch_result
    return cursor
