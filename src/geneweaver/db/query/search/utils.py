"""Functions for generating search queries."""
from typing import Tuple

from psycopg.sql import SQL, Composed
from enum import Enum


class SearchConfig(Enum):
    """Search configuration options."""

    SIMPLE = "simple"
    ENGLISH = "english"

    def __str__(self) -> str:
        return self.value


class QueryType(Enum):
    """Postgresql Query Type."""

    PLAINTO = "plainto_tsquery"
    PHRASETO = "phraseto_tsquery"
    WEBSEARCH = "websearch_to_tsquery"


def search_query(
    search_column: str,
    search_string: str,
    search_config: SearchConfig = SearchConfig.SIMPLE,
    query_type: QueryType = QueryType.WEBSEARCH,
) -> Tuple[Composed, dict]:
    query = SQL(
        "{search_column} @@ {query_type}('{search_config}', '$(search)s')"
    ).format(
        search_column=search_column,
        query_type=str(query_type),
        search_config=str(search_config),
    )
    return query, {"search": search_string}
