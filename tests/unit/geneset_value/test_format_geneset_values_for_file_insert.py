"""Test the format_geneset_values_for_file_insert function."""
import pytest
from geneweaver.db.geneset_value import (
    GenesetValueInput,
    format_geneset_values_for_file_insert,
)


@pytest.mark.parametrize(
    ("geneset_values", "expected_result"),
    [
        # Test with empty list
        ([], ""),
        # Test with single GenesetValueInput
        ([GenesetValueInput(symbol="symbol1", value=1.0)], "symbol1\t1.0"),
        ([GenesetValueInput(symbol="symbol2", value=2.0)], "symbol2\t2.0"),
        ([GenesetValueInput(symbol="symbol3", value=3.0)], "symbol3\t3.0"),
        # Test with multiple GenesetValueInput
        (
            [
                GenesetValueInput(symbol="symbol1", value=1.0),
                GenesetValueInput(symbol="symbol2", value=2.0),
                GenesetValueInput(symbol="symbol3", value=3.0),
            ],
            "symbol1\t1.0\nsymbol2\t2.0\nsymbol3\t3.0",
        ),
        # Try the same values but in a different order
        (
            [
                GenesetValueInput(symbol="symbol3", value=3.0),
                GenesetValueInput(symbol="symbol1", value=1.0),
                GenesetValueInput(symbol="symbol2", value=2.0),
            ],
            "symbol3\t3.0\nsymbol1\t1.0\nsymbol2\t2.0",
        ),
        # Test with negative values
        ([GenesetValueInput(symbol="symbol1", value=-1.0)], "symbol1\t-1.0"),
        # Test with zero value
        ([GenesetValueInput(symbol="symbol1", value=0.0)], "symbol1\t0.0"),
        # Test with decimal values
        ([GenesetValueInput(symbol="symbol1", value=1.23)], "symbol1\t1.23"),
        # Test with large values
        ([GenesetValueInput(symbol="symbol1", value=1000000.0)], "symbol1\t1000000.0"),
        # Test with very small values
        ([GenesetValueInput(symbol="symbol1", value=0.000001)], "symbol1\t1e-06"),
        # Test with high precision values
        (
            [GenesetValueInput(symbol="Trio", value=0.0001928920607716660)],
            "Trio\t0.000192892060771666",
        ),
        (
            [GenesetValueInput(symbol="Mapt", value=0.0001979595721433030)],
            "Mapt\t0.000197959572143303",
        ),
        (
            [GenesetValueInput(symbol="1110013G13Rik", value=0.0002014711275497570)],
            "1110013G13Rik\t0.000201471127549757",
        ),
        # Test with symbols containing special characters
        ([GenesetValueInput(symbol="sym$bol1", value=1.0)], "sym$bol1\t1.0"),
        ([GenesetValueInput(symbol="symbol#", value=1.0)], "symbol#\t1.0"),
        ([GenesetValueInput(symbol="sym*bol1", value=1.0)], "sym*bol1\t1.0"),
        # Test with symbols containing spaces
        ([GenesetValueInput(symbol="symbol 1", value=1.0)], "symbol 1\t1.0"),
    ],
)
def test_format_geneset_values_for_file_insert(geneset_values, expected_result):
    """Test that the geneset values function formats as expected."""
    result = format_geneset_values_for_file_insert(geneset_values)
    assert result == expected_result
