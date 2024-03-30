"""Test the publication.add query generation function."""

import pytest
from geneweaver.db.query.publication import add
from psycopg.sql import SQL, Composed, Identifier, Placeholder


@pytest.mark.parametrize(
    "authors",
    ["Author 1", "Author 1, Author 2", "Author 1, Author 2, Author 3, et al."],
)
@pytest.mark.parametrize(
    "title", ["Title 1", "Title 1: Subtitle", "Title 1: Subtitle, Part 2"]
)
@pytest.mark.parametrize(
    "abstract",
    [
        "Abstract 1",
        "Abstract 1: Subabstract",
        "Abstract 1: Subabstract, Part 2",
        "A very long abstract" * 100,
    ],
)
@pytest.mark.parametrize(
    "journal", ["Journal 1", "Journal 1: Subjournal", "Journal 1: Subjournal, Part 2"]
)
@pytest.mark.parametrize(
    "pubmed_id", ["12345678", "23456789", "34567890", "45678901", "1234"]
)
def test_add_types(authors, title, abstract, journal, pubmed_id):
    """Test the add query generation function."""
    query, params = add(authors, title, abstract, journal, pubmed_id)
    assert isinstance(query, Composed)
    assert isinstance(params, dict)
    for item in query:
        assert any(
            isinstance(item, t) for t in [SQL, Composed, Identifier, Placeholder]
        )

    for item in params.values():
        if item is not None:
            assert isinstance(item, str)
            assert item in [authors, title, abstract, journal, pubmed_id]

    values = [item for item in params.values() if item is not None]
    assert len(values) == 5
    assert authors in values
    assert title in values
    assert abstract in values
    assert journal in values
    assert pubmed_id in values
