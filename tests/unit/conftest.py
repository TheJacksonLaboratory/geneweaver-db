"""Fixtures for all db unit tests."""

import random
from unittest.mock import AsyncMock, MagicMock

import pytest
from psycopg import AsyncCursor, Cursor

from tests.unit.const import (
    PSYCOPG_ALL_ERRORS,
    PSYCOPG_BASE_ERRORS,
)
from tests.unit.geneset.const import GENESET_CURATION_IDS, GENESETS


@pytest.fixture(params=PSYCOPG_ALL_ERRORS)
def all_psycopg_errors(request):
    """Return all psycopg errors."""
    return request.param


@pytest.fixture(params=PSYCOPG_BASE_ERRORS)
def base_psycopg_errors(request):
    """Return base psycopg errors."""
    return request.param


# We want random but repeatable tests.
random.seed(0)

# Some small primary keys, and some big ones.
EXAMPLE_PRIMARY_KEYS = [0, 1, 2, 3, 10, 100] + sorted(
    random.sample(range(100, 500150300), 10)
)

# Like the PRIMARY_KEYS, but a bit smaller.
EXAMPLE_USER_IDS = [1, 2, 3, 10, 100] + sorted(random.sample(range(100, 250300), 10))


@pytest.fixture(params=EXAMPLE_PRIMARY_KEYS)
def example_primary_key(request):
    """Return an example primary key."""
    return request.param


@pytest.fixture(params=EXAMPLE_USER_IDS)
def example_user_id(request):
    """Return an example user id."""
    return request.param


@pytest.fixture(params=GENESETS)
def example_geneset(request):
    """Return an example geneset."""
    return request.param


@pytest.fixture(
    params=[]
    + [GENESETS]
    + [GENESETS[0]]
    + [GENESETS[1:]]
    + [GENESETS[0:2]]
    + [GENESETS[0:3]]
    + [GENESETS[0:4]]
)
def example_genesets(request):
    """Return an example geneset."""
    return request.param


@pytest.fixture(params=GENESET_CURATION_IDS)
def geneset_curation_id(request):
    """Return one of the geneset curation ids."""
    return request.param


@pytest.fixture()
def cursor(request):
    """Create a magic mock cursor."""
    return MagicMock(spec=Cursor)


@pytest.fixture()
def cursor_execute_raises_error(cursor, all_psycopg_errors):
    """Create a magic mock cursor that raises an error when execute is called."""
    cursor.execute.side_effect = all_psycopg_errors("Error message")
    return cursor


@pytest.fixture()
def cursor_fetchone_raises_error(cursor, all_psycopg_errors):
    """Create a magic mock cursor that raises an error when fetchone is called."""
    cursor.fetchone.side_effect = all_psycopg_errors("Error message")
    return cursor


@pytest.fixture()
def cursor_fetchall_raises_error(cursor, all_psycopg_errors):
    """Create a magic mock cursor that raises an error when fetchall is called."""
    cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    return cursor


@pytest.fixture()
def async_cursor(request):
    """Create a magic mock async cursor."""
    return AsyncMock(spec=AsyncCursor)


@pytest.fixture()
def async_cursor_execute_raises_error(async_cursor, all_psycopg_errors):
    """Create a magic mock cursor that raises an error when execute is called."""
    async_cursor.execute.side_effect = all_psycopg_errors("Error message")
    return async_cursor


@pytest.fixture()
def async_cursor_fetchone_raises_error(async_cursor, all_psycopg_errors):
    """Create a magic mock cursor that raises an error when fetchone is called."""
    async_cursor.fetchone.side_effect = all_psycopg_errors("Error message")
    return async_cursor


@pytest.fixture()
def async_cursor_fetchall_raises_error(async_cursor, all_psycopg_errors):
    """Create a magic mock cursor that raises an error when fetchall is called."""
    async_cursor.fetchall.side_effect = all_psycopg_errors("Error message")
    return async_cursor
