"""Test the geneset.write.add_geneset_file query generation function."""

import pytest
from geneweaver.db.query.geneset.write import add_geneset_file
from psycopg.sql import SQL


@pytest.mark.parametrize("size", [0, 1, 10, 100, 1000])
@pytest.mark.parametrize("comments", [None, "", "comment1\ncomment2\n", "comment3\n"])
@pytest.mark.parametrize(
    "contents", ["gene1\t1.0\ngene2\t2.0", "gene3\t3.0\ngene4\t4.0"]
)
def test_add_geneset_file(size, comments, contents):
    """Test the add_geneset_file query generation function."""
    query, params = add_geneset_file(
        size=size,
        comments=comments,
        contents=contents,
    )

    for item in query:
        assert isinstance(item, SQL)

    assert params == {
        "file_size": size,
        "file_comments": comments,
        "file_contents": contents,
    }
