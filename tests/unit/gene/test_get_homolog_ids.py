"""Test the get_homolog_ids function."""
from unittest.mock import Mock, patch

import pytest
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.gene import get_homolog_ids

IDENTIFIERS = [identifier for identifier in GeneIdentifier]
SPECIES = [species for species in Species]


@pytest.mark.parametrize("source_identifier", IDENTIFIERS)
def test_no_optional_args(cursor, source_identifier):
    """Test the get_homolog_ids function with no optional arguments.

    This should result in a call to cursor.execute with a param dict with only two
    keys: "source_ids" and "result_genedb_id".
    """
    with patch("geneweaver.db.gene.SQL") as mock_sql:
        mock_sql.return_value = "mock query"
        cursor.execute = Mock()
        get_homolog_ids(cursor, ("1", "2"), source_identifier)
        assert mock_sql.call_count == 1
        cursor.execute.assert_called_once_with(
            "mock query",
            {
                "source_ids": ["1", "2"],
                "result_genedb_id": source_identifier.value,
            },
        )


@pytest.mark.parametrize("result_identifier", IDENTIFIERS)
@pytest.mark.parametrize("source_identifier", IDENTIFIERS)
def test_with_source_identifier(cursor, result_identifier, source_identifier):
    """Test the get_homolog_ids function with a source identifier.

    This should result in a call to cursor.execute with a param dict with three
    keys: "source_ids", "result_genedb_id", and "source_genedb_id".
    """
    with patch("geneweaver.db.gene.SQL") as mock_sql:
        mock_sql.return_value = "mock query"
        cursor.execute = Mock()
        get_homolog_ids(
            cursor,
            ("1", "2"),
            result_identifier,
            source_identifier=source_identifier,
        )
        assert mock_sql.call_count == 2
        cursor.execute.assert_called_once_with(
            "mock query" * 2,
            {
                "source_ids": ["1", "2"],
                "result_genedb_id": result_identifier.value,
                "source_genedb_id": source_identifier.value,
            },
        )


@pytest.mark.parametrize("result_identifier", IDENTIFIERS)
@pytest.mark.parametrize("result_species", SPECIES)
def test_with_result_species(cursor, result_identifier, result_species):
    """Test the get_homolog_ids function with a result species.

    This should result in a call to cursor.execute with a param dict with three
    keys: "source_ids", "result_genedb_id", and "result_sp_id".
    """
    with patch("geneweaver.db.gene.SQL") as mock_sql:
        mock_sql.return_value = "mock query"
        cursor.execute = Mock()
        get_homolog_ids(
            cursor,
            ("1", "2"),
            result_identifier,
            result_species=result_species,
        )
        assert mock_sql.call_count == 2
        cursor.execute.assert_called_once_with(
            "mock query" * 2,
            {
                "source_ids": ["1", "2"],
                "result_genedb_id": result_identifier.value,
                "result_sp_id": result_species.value,
            },
        )


@pytest.mark.parametrize("result_identifier", IDENTIFIERS)
@pytest.mark.parametrize("source_species", SPECIES)
def test_with_source_species(cursor, result_identifier, source_species):
    """Test the get_homolog_ids function with a source species."""
    with patch("geneweaver.db.gene.SQL") as mock_sql:
        mock_sql.return_value = "mock query"
        cursor.execute = Mock()
        get_homolog_ids(
            cursor,
            ("1", "2"),
            result_identifier,
            source_species=source_species,
        )
        assert mock_sql.call_count == 2
        cursor.execute.assert_called_once_with(
            "mock query" * 2,
            {
                "source_ids": ["1", "2"],
                "result_genedb_id": result_identifier.value,
                "source_sp_id": source_species.value,
            },
        )


@pytest.mark.parametrize("source_identifier", IDENTIFIERS)
@pytest.mark.parametrize("result_species", SPECIES)
@pytest.mark.parametrize("source_species", SPECIES)
def test_with_all_args(cursor, source_identifier, result_species, source_species):
    """Test the get_homolog_ids function with all optional arguments."""
    with patch("geneweaver.db.gene.SQL") as mock_sql:
        mock_sql.return_value = "mock query"
        cursor.execute = Mock()
        get_homolog_ids(
            cursor,
            ("1", "2"),
            GeneIdentifier.ENSEMBLE_GENE,
            source_identifier=source_identifier,
            result_species=result_species,
            source_species=source_species,
        )
        assert mock_sql.call_count == 4
        cursor.execute.assert_called_once_with(
            "mock query" * 4,
            {
                "source_ids": ["1", "2"],
                "result_genedb_id": GeneIdentifier.ENSEMBLE_GENE.value,
                "source_genedb_id": source_identifier.value,
                "result_sp_id": result_species.value,
                "source_sp_id": source_species.value,
            },
        )
