"""Test the internal _search function for geneset sql generation."""

import pytest
from geneweaver.db.query.geneset.utils import search


@pytest.mark.parametrize("filters", [[], ["A"], ["A", "B", "C", "D"]])
@pytest.mark.parametrize("params", [{}, {"gs_id": 1}, {"gs_id": 1, "user_id": 1}])
@pytest.mark.parametrize(
    "search_text", [None, "test", "test search", "test search text"]
)
def test_search(filters, params, search_text):
    """Test the internal _search function for geneset sql generation."""
    result = search(filters, params, search_text)
    assert result is not None

    filters_copy = filters.copy()
    params_copy = params.copy()

    if search_text is not None:
        assert "search" in str(result[-1])
        assert result[1]["search"] == search_text
    else:
        assert filters_copy == filters
        assert params_copy == params
