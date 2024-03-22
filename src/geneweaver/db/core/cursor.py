"""Convenience code for interacting with the database."""

from contextlib import asynccontextmanager, contextmanager

import psycopg
from geneweaver.db.core.settings import settings


@contextmanager
def cursor() -> psycopg.Cursor:
    """Get a cursor to the database."""
    with psycopg.connect(settings.URI) as connection:
        with connection.cursor() as _cursor:
            yield _cursor


@asynccontextmanager
async def async_cursor() -> psycopg.AsyncCursor:
    async with await psycopg.AsyncConnection.connect(settings.URI) as connection:
        async with connection.cursor() as _cursor:
            yield _cursor


def make_connection():
    return psycopg.connect(settings.URI)
