"""Utilities for testing the database module."""
# ruff: noqa: ANN002, ANN003, ANN101, D102, D107
from typing import Callable
from unittest.mock import MagicMock

import pytest
from psycopg import Cursor


def get_magic_mock_cursor(fetch_result) -> MagicMock:
    """Return a mock cursor with the given fetch result."""
    cursor = MagicMock(spec=Cursor)
    cursor.fetchone.return_value = fetch_result
    cursor.fetchall.return_value = fetch_result
    return cursor


def create_execute_raises_error_test(function, *args, **kwargs) -> Callable:
    """Return a test function that tests the execute error path."""

    def test_function(all_psycopg_errors, cursor_execute_raises_error) -> None:
        with pytest.raises(all_psycopg_errors, match="Error message"):
            function(cursor_execute_raises_error, *args, **kwargs)
        assert cursor_execute_raises_error.execute.call_count == 1
        assert cursor_execute_raises_error.fetchone.call_count == 0
        assert cursor_execute_raises_error.fetchall.call_count == 0

    test_function.__name__ = f"test_{function.__name__}_execute_raises_error"

    return test_function


def create_fetchone_raises_error_test(function, *args, **kwargs) -> Callable:
    """Return a test function that tests the fetchone error path."""

    def test_function(all_psycopg_errors, cursor_fetchone_raises_error) -> None:
        with pytest.raises(all_psycopg_errors, match="Error message"):
            function(cursor_fetchone_raises_error, *args, **kwargs)
        assert cursor_fetchone_raises_error.execute.call_count == 1
        assert cursor_fetchone_raises_error.fetchone.call_count == 1
        assert cursor_fetchone_raises_error.fetchall.call_count == 0

    test_function.__name__ = f"test_{function.__name__}_fetchone_raises_error"

    return test_function


def create_fetchall_raises_error_test(function, *args, **kwargs) -> Callable:
    """Return a test function that tests the fetchall error path."""

    def test_function(all_psycopg_errors, cursor_fetchall_raises_error) -> None:
        with pytest.raises(all_psycopg_errors, match="Error message"):
            function(cursor_fetchall_raises_error, *args, **kwargs)
        assert cursor_fetchall_raises_error.execute.call_count == 1
        assert cursor_fetchall_raises_error.fetchone.call_count == 0
        assert cursor_fetchall_raises_error.fetchall.call_count == 1

    test_function.__name__ = f"test_{function.__name__}_fetchall_raises_error"

    return test_function
