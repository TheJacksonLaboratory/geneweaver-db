"""Test the get_publication_by_pubmed_id function."""
import pytest
from geneweaver.db.publication import (
    get_publication_by_pubmed_id,
)

from tests.unit.publication.const import (
    EDGE_CASE_PUBMED_PUBLICATIONS,
    PUBMED_PUBLICATIONS,
)
from tests.unit.testing_utils import get_magic_mock_cursor


@pytest.mark.parametrize(
    ("pmid", "expected_result"), PUBMED_PUBLICATIONS + EDGE_CASE_PUBMED_PUBLICATIONS
)
def test_get_publication_by_pubmed_id(pmid, expected_result):
    """Test getting a publication by pubmed id."""
    # Prepare the mock cursor
    cursor = get_magic_mock_cursor(expected_result)

    result = get_publication_by_pubmed_id(cursor, pmid)

    assert result == expected_result
    assert "publication" in cursor.execute.call_args[0][0]
    assert pmid in cursor.execute.call_args[0][1]
