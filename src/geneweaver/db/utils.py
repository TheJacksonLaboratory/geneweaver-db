"""Utilities for the GeneWeaver database functions."""
# ruff: noqa: ANN001, ANN002, ANN003, ANN201, ANN202
import functools
from typing import List, Optional

from geneweaver.db.exceptions import GeneweaverDoesNotExistError, GeneweaverValueError
from psycopg import sql
from psycopg.rows import Row


def unpack_one_item_fetchall_results(results: List[Row]) -> List:
    """Unpack a single column from multiple rows of results.

    :param results: The results from a fetchall call.

    :raises GeneweaverDoesNotExistError: If the result is empty.
    :raises GeneweaverTooManyResultsError: If the result has more than one row.

    :return: The single row from the results.
    """
    if len(results) == 0:
        raise GeneweaverDoesNotExistError("No results found.")

    if len(results[0]) > 1:
        raise GeneweaverValueError("Too many results to unpack.")

    return [t[0] for t in results]


def temp_override_row_factory(row_factory):
    """Temporarily override the row factory for a function.

    This is useful for functions that use a cursor as an argument, but which process
    cursor results internally and therefore need a specific row factory to be set.

    :param row_factory: The row factory to use.

    :return: The function wrapper.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine cursor based on positional or keyword argument
            if args:
                cursor = args[0]
            else:
                cursor = kwargs.get("cursor")

            if cursor is None:
                raise ValueError(
                    "Cursor must be provided either as a "
                    "positional or keyword argument."
                )

            original_row_factory = cursor.row_factory
            cursor.row_factory = row_factory

            try:
                result = func(*args, **kwargs)
            finally:
                cursor.row_factory = original_row_factory

            return result

        return wrapper

    return decorator


def format_sql_fields(
    fields_map: dict,
    query_table: Optional[str] = None,
    resp_prefix: Optional[str] = None,
) -> List[sql.Composed]:
    """Format SQL fields for a query."""
    select_prefix = query_table or ""
    resp_prefix = resp_prefix or ""

    return [
        sql.SQL("{select_prefix}.{field} AS {resp_prefix}_{field}").format(
            select_prefix=sql.Identifier(select_prefix),
            resp_prefix=sql.Identifier(resp_prefix),
            field=sql.Identifier(field),
        )
        for field in fields_map.keys()
    ]
