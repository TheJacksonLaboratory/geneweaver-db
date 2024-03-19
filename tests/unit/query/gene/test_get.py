"""Test the gene `get` query function generation function."""

import pytest
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.query.gene import get


@pytest.mark.parametrize("gene_id", [None, 1, 12345])
@pytest.mark.parametrize(
    "reference_id", [None, "ENSG00000139618", "ENSG00000139618.12"]
)
@pytest.mark.parametrize("gene_database", [None, GeneIdentifier.ENSEMBLE_GENE])
@pytest.mark.parametrize("species", [None, Species.HOMO_SAPIENS])
@pytest.mark.parametrize("preferred", [None, True, False])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
def test_all_kwargs(
    gene_id, reference_id, gene_database, species, preferred, limit, offset
):
    """Test all the kwarg combinations for query.gene.get."""
    query, params = get(
        gene_id=gene_id,
        reference_id=reference_id,
        gene_database=gene_database,
        species=species,
        preferred=preferred,
        limit=limit,
        offset=offset,
    )

    if gene_id is not None:
        assert "gene_id" in params
    else:
        assert "gene_id" not in params

    if reference_id is not None:
        assert "ref_id" in params
    else:
        assert "ref_id" not in params

    if gene_database is not None:
        assert "gene_db_id" in params
    else:
        assert "gene_db_id" not in params

    if species is not None:
        assert "species_id" in params
    else:
        assert "species_id" not in params

    if preferred is not None:
        assert "preferred" in params
    else:
        assert "preferred" not in params
