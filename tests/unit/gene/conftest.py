import random
import pytest
from typing import List

from tests.unit.gene.const import GENE_SYMBOLS_01, GENE_SYMBOLS_02

# We want some randomness, but we want it to be repeatable
random.seed(0)


@pytest.fixture(params=list(range(1, 250)))
def geneset_gene_symbols(request) -> List[str]:
    """Return a list of geneset genes."""
    return random.sample(GENE_SYMBOLS_01 + GENE_SYMBOLS_02, request.param)
