"""Test the get_homolog_ids function."""
from unittest.mock import Mock, patch

from geneweaver.core.enum import GeneIdentifier
from geneweaver.db.gene import get_homolog_ids


@patch("geneweaver.db.gene.get_homolog_ids_with_source_identifier")
@patch("geneweaver.db.gene.get_homolog_ids_without_source_identifier")
def test_without_source_identifier(mock_without, mock_with):
    """Test that the get_homolog_ids function calls the correct function w source."""
    cursor = Mock()
    _ = get_homolog_ids(
        cursor, ("1", "2"), result_identifier=GeneIdentifier.ENSEMBLE_GENE
    )
    mock_without.assert_called_once_with(
        cursor, ("1", "2"), result_identifier=GeneIdentifier.ENSEMBLE_GENE
    )
    assert mock_with.call_count == 0
    assert mock_without.call_count == 1


@patch("geneweaver.db.gene.get_homolog_ids_with_source_identifier")
@patch("geneweaver.db.gene.get_homolog_ids_without_source_identifier")
def test_with_source_identifier(mock_without, mock_with):
    """Test that the get_homolog_ids function calls the correct function with source."""
    cursor = Mock()
    _ = get_homolog_ids(
        cursor,
        ("1", "2"),
        result_identifier=GeneIdentifier.ENSEMBLE_GENE,
        source_identifier=GeneIdentifier.GENE_SYMBOL,
    )
    mock_with.assert_called_once_with(
        cursor,
        ("1", "2"),
        result_identifier=GeneIdentifier.ENSEMBLE_GENE,
        source_identifier=GeneIdentifier.GENE_SYMBOL,
    )
    assert mock_with.call_count == 1
    assert mock_without.call_count == 0
