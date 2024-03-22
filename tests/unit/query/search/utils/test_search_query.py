"""Test the query generation search_query util function."""

import pytest
from geneweaver.db.query.search.utils import search_query
from psycopg.sql import SQL, Composed, Identifier


@pytest.mark.parametrize(
    "search_column",
    [
        SQL("name"),
        Identifier("description"),
        SQL("tags"),
        (SQL("owner") + SQL("column")),
        Identifier("genes"),
    ],
)
@pytest.mark.parametrize("search_config", ["simple", "english"])
def test_search_query_required_args(search_column, search_config):
    """Test the search_query function."""
    result = search_query(search_column, search_config)
    assert search_config in str(result)

    if isinstance(search_column, Composed):
        for item in search_column:
            assert str(item) in str(result)
    else:
        assert str(search_column) in str(result)
