"""Fixtures for all db unit tests."""
import pytest

from tests.unit.const import (
    PSYCOPG_ALL_ERRORS,
    PSYCOPG_BASE_ERRORS,
)


@pytest.fixture(params=PSYCOPG_ALL_ERRORS)
def all_psycopg_errors(request):
    """Return all psycopg errors."""
    return request.param


@pytest.fixture(params=PSYCOPG_BASE_ERRORS)
def base_psycopg_errors(request):
    """Return base psycopg errors."""
    return request.param
