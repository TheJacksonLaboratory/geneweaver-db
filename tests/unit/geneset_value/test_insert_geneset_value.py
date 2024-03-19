"""Test the insert_geneset_value function."""

import pytest
from geneweaver.db.geneset_value import insert_geneset_value

from tests.unit.testing_utils import get_magic_mock_cursor


@pytest.mark.parametrize(
    (
        "geneset_id",
        "gene_id",
        "value",
        "name",
        "within_threshold",
        "fetch_result",
        "expected_result",
    ),
    [
        # Test case 1
        (
            1,  # geneset_id
            2,  # gene_id
            "3.5",  # value
            "gene1",  # name
            True,  # within_threshold
            (10,),  # fetch_result
            10,  # expected_result
        ),
        # Test case 2
        (
            5,  # geneset_id
            6,  # gene_id
            "7.5",  # value
            "gene2",  # name
            False,  # within_threshold
            (20,),  # fetch_result
            20,  # expected_result
        ),
        # Add more test cases as needed
    ],
)
def test_insert_geneset_value(
    geneset_id, gene_id, value, name, within_threshold, fetch_result, expected_result
):
    """Test the happy path using a mock cursor."""
    mock_cursor = get_magic_mock_cursor(fetch_result)
    result = insert_geneset_value(
        mock_cursor, geneset_id, gene_id, value, name, within_threshold
    )
    assert result == expected_result
