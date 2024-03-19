"""Tests for the search query util enums module."""

import pytest
from geneweaver.db.query.search.utils import (
    QueryType,
    SearchConfig,
)


@pytest.mark.parametrize(
    ("search_config", "expected"),
    [
        (SearchConfig.SIMPLE, "simple"),
        (SearchConfig.ENGLISH, "english"),
    ],
)
def test_search_config_enum(search_config, expected):
    """Test the search config enum."""
    assert str(search_config) == expected
    assert SearchConfig(expected) == search_config


@pytest.mark.parametrize(
    ("query_type", "expected"),
    [
        (QueryType.PLAINTO, "plainto_tsquery"),
        (QueryType.PHRASETO, "phraseto_tsquery"),
        (QueryType.WEBSEARCH, "websearch_to_tsquery"),
    ],
)
def test_query_type_enum(query_type, expected):
    """Test the query type enum."""
    assert str(query_type) == expected
    assert QueryType(expected) == query_type
