"""Test the get_publication_by_pubmed_id function."""
import pytest
from geneweaver.db.publication import by_pubmed_id

from tests.unit.publication.const import (
    EDGE_CASE_PUBMED_PUBLICATIONS,
    PUBMED_PUBLICATIONS,
)
from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
    get_magic_mock_cursor,
)

test_by_pubmed_id_execute_raises_error = create_execute_raises_error_test(
    by_pubmed_id, "12345678"
)

test_by_pubmed_id_fetchone_raises_error = create_fetchone_raises_error_test(
    by_pubmed_id, "12345678"
)


@pytest.mark.parametrize(
    ("pmid", "expected_result"), PUBMED_PUBLICATIONS + EDGE_CASE_PUBMED_PUBLICATIONS
)
def test_get_publication_by_pubmed_id(pmid, expected_result):
    """Test getting a publication by pubmed id."""
    # Prepare the mock cursor
    cursor = get_magic_mock_cursor(expected_result)

    result = by_pubmed_id(cursor, pmid)

    assert result == expected_result
    assert pmid in cursor.execute.call_args[0][1].values()
