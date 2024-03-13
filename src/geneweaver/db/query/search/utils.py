"""Functions for generating search queries."""
from enum import Enum
from typing import Tuple

from psycopg.sql import SQL, Composed


class SearchConfig(Enum):
    """Search configuration options."""

    SIMPLE = "simple"
    ENGLISH = "english"

    def __str__(self: "SearchConfig") -> str:
        """Render the value as a string."""
        return self.value


class QueryType(Enum):
    """Postgresql Query Type."""

    PLAINTO = "plainto_tsquery"
    PHRASETO = "phraseto_tsquery"
    WEBSEARCH = "websearch_to_tsquery"

    def __str__(self: "SearchConfig") -> str:
        """Render the value as a string."""
        return self.value


def search_query(
    search_column: str,
    search_string: str,
    search_config: SearchConfig = SearchConfig.SIMPLE,
    query_type: QueryType = QueryType.WEBSEARCH,
) -> Tuple[Composed, dict]:
    """Generate a search query.

    Works generically with any table that has a search column.

    :param search_column: The column to search.
    :param search_string: The string to search for.
    :param search_config: The search configuration to use.
    :param query_type: The query type to use.
    """
    query = SQL(
        "{search_column} @@ {query_type}('{search_config}', '$(search)s')"
    ).format(
        search_column=search_column,
        query_type=str(query_type),
        search_config=str(search_config),
    )
    return query, {"search": search_string}
