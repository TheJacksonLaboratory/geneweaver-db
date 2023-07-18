import random

import pytest
from geneweaver.db.publication import (
    get_publications_by_pubmed_ids,
)

from tests.unit.publication.const import (
    EDGE_CASE_PUBMED_PUBLICATIONS,
    PUBMED_PUBLICATIONS,
)
from tests.unit.db.utils import get_magic_mock_cursor

# We want repeatable tests, so let's set the random seed.
random.seed(1)

# Let's generate "random" subsets of our example publications.
PUBLICATIONS = PUBMED_PUBLICATIONS + EDGE_CASE_PUBMED_PUBLICATIONS
# We want to test a variety of lengths, so let's generate a list of lengths.
lengths = [random.randint(1, len(PUBLICATIONS)) for _ in range(30)]
# Now let's generate a list of subsets of our publications.
subsets = [random.sample(PUBLICATIONS, length) for length in lengths]
# Now we unpack the subsets into a tuple of pubmed ids and a tuple of expected results.
params = [[l for l in zip(*subset)] for subset in subsets]


@pytest.mark.parametrize(("pmids", "expected_result"), params)
def test_get_publications_by_pubmed_ids(pmids, expected_result):
    # Prepare the mock cursor
    cursor = get_magic_mock_cursor(expected_result)

    result = get_publications_by_pubmed_ids(cursor, pmids)

    assert result == expected_result
    assert 'publication' in cursor.execute.call_args[0][0]
    for pmid in pmids:
        assert pmid in cursor.execute.call_args[0][1][0]
