"""Test the render_and_add_geneset_file query generation function."""

from unittest.mock import patch

import pytest
from geneweaver.core.schema.gene import GeneValue
from geneweaver.db.query.geneset import render_and_add_geneset_file


@pytest.mark.parametrize(
    ("gene_values", "expected_contents", "expected_size"),
    [
        (
            [
                GeneValue(symbol="gene1", value=1.0),
                GeneValue(symbol="gene2", value=2.0),
            ],
            "gene1\t1.0\ngene2\t2.0",
            19,
        ),
        (
            [
                GeneValue(symbol="gene3", value=3.0),
                GeneValue(symbol="gene4", value=4.0),
            ],
            "gene3\t3.0\ngene4\t4.0",
            19,
        ),
        (
            [
                GeneValue(symbol="gene5", value=5.0),
                GeneValue(symbol="gene6", value=6.0),
            ],
            "gene5\t5.0\ngene6\t6.0",
            19,
        ),
        (
            [GeneValue(symbol="gene7", value=7.0), GeneValue(symbol="gene8", value=8.0)]
            * 100,
            "\n".join("gene7\t7.0\ngene8\t8.0" for _ in range(100)),
            1999,
        ),
        (
            [GeneValue(symbol="gene7", value=7.0), GeneValue(symbol="gene8", value=8.0)]
            * 1000,
            "\n".join("gene7\t7.0\ngene8\t8.0" for _ in range(1000)),
            19999,
        ),
    ],
)
@pytest.mark.parametrize(
    "comments",
    [
        None,
        "",
        "comment1\ncomment2\n",
        "comment3\n",
        "\n".join(["A really long comment" for _ in range(100)]),
        "A \t comment \r\n with \n special \t characters \r\n",
    ],
)
def test_render_and_add_geneset_file(
    gene_values, expected_contents, expected_size, comments
):
    """Test the render_and_add_geneset_file query generation function."""
    with patch(
        "geneweaver.db.query.geneset.write.add_geneset_file"
    ) as mock_add_geneset_file:
        print(mock_add_geneset_file)
        result = render_and_add_geneset_file(gene_values, comments)
        print(result)
        assert mock_add_geneset_file.call_count == 1
        assert expected_size == mock_add_geneset_file.call_args[0][0]
        assert expected_contents == mock_add_geneset_file.call_args[0][1]
        assert comments == mock_add_geneset_file.call_args[0][2]
