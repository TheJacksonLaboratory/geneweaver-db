"""Test the geneset.write.add query generation function."""

from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.db.query.geneset.write import add
from psycopg.sql import SQL, Composed, Identifier, Placeholder


def test_geneset_add():
    """Test the add geneset query generation function."""
    query, params = add(
        user_id=1,
        file_id=1,
        name="a string",
        abbreviation="a string",
        publication_id=1,
        tier=GenesetTier.TIER1,
        description="a string",
        species=Species.MUS_MUSCULUS,
        count=1,
        threshold_type="a string",
        threshold=1.0,
        gene_id_type=GeneIdentifier.GENE_SYMBOL,
        attribution="a string",
    )
    for item in query:
        assert any(
            isinstance(item, t) for t in [SQL, Composed, Identifier, Placeholder]
        )
