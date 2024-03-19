"""Test the species `get` query function generation function."""

import pytest
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.query.species import get


@pytest.mark.parametrize("taxonomic_id", [None, 1])
@pytest.mark.parametrize("reference_gene_db_id", [None, GeneIdentifier.HGNC])
@pytest.mark.parametrize("species", [None, Species.HOMO_SAPIENS])
def test_all_kwargs(taxonomic_id, reference_gene_db_id, species):
    """Test all the kwarg combinations for query.species.get."""
    query, params = get(
        taxonomic_id=taxonomic_id,
        reference_gene_db_id=reference_gene_db_id,
        species=species,
    )

    if taxonomic_id is not None:
        assert "taxonomic_id" in params

    if species is not None:
        assert "species_id" in params

    if reference_gene_db_id is not None:
        assert "reference_gene_db_id" in params
