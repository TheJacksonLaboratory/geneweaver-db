import pytest
from geneweaver.db.geneset_value import (
    format_geneset_values_for_file_insert,
    GenesetValueInput
)


@pytest.mark.parametrize(
    "geneset_values, expected_result",
    [
        # Test with empty list
        ([], ""),

        # Test with single GenesetValueInput
        ([GenesetValueInput(symbol='symbol1', value=1.0)], "symbol1\t1.0"),

        # Test with multiple GenesetValueInput
        (
            [
                GenesetValueInput(symbol='symbol1', value=1.0),
                GenesetValueInput(symbol='symbol2', value=2.0),
                GenesetValueInput(symbol='symbol3', value=3.0)
            ],
            "symbol1\t1.0\nsymbol2\t2.0\nsymbol3\t3.0"
        ),
        # Add more test cases as needed
    ],
)
def test_format_geneset_values_for_file_insert(geneset_values, expected_result):
    result = format_geneset_values_for_file_insert(geneset_values)
    assert result == expected_result
