"""Test the publication.get query function."""
import pytest

from geneweaver.db.query.publication import get


def test_get_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        _ = get()
