"""Test the query generation search_query util function."""
import pytest
from geneweaver.db.query.search.utils import search_query


@pytest.mark.parametrize(
    "search_column", ["name", "description", "tags", "owner", "genes"]
)
@pytest.mark.parametrize("search_config", ["simple", "english"])
def test_search_query_required_args(search_column, search_config):
    """Test the search_query function."""
    result = search_query(search_column, search_config)
    assert search_column in str(result)
    assert search_config in str(result)
