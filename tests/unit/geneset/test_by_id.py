"""Test the geneset.by_id function."""

import pytest
from geneweaver.db.geneset import by_id

from tests.unit.geneset.const import GENESETS
from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)


@pytest.mark.parametrize("geneset", GENESETS)
def test_by_id(geneset, cursor):
    """Test the geneset.by_id function."""
    cursor.fetchone.return_value = geneset
    result = by_id(cursor, geneset["gs_id"])
    assert result == geneset
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


@pytest.mark.parametrize("with_publication_info", [True, False])
@pytest.mark.parametrize("geneset", GENESETS)
def test_by_id__pub_info_kwarg(with_publication_info, geneset, cursor):
    """Test the geneset.by_id function with publication info kwarg."""
    cursor.fetchone.return_value = geneset
    result = by_id(
        cursor, geneset["gs_id"], with_publication_info=with_publication_info
    )
    assert result == geneset
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


@pytest.mark.parametrize("with_publication_info", [True, False])
@pytest.mark.parametrize("geneset", GENESETS)
def test_by_id__pub_info_arg(with_publication_info, geneset, cursor):
    """Test the geneset.by_id function with publication info arg."""
    cursor.fetchone.return_value = geneset
    result = by_id(cursor, geneset["gs_id"], with_publication_info)
    assert result == geneset
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.fetchall.call_count == 0


test_by_id_execute_raises_error = create_execute_raises_error_test(by_id, 1)

test_by_id_fetchone_raises_error = create_fetchone_raises_error_test(by_id, 1)
