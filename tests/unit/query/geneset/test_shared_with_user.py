"""Test the geneset.shared_with_user query function."""

import pytest
from geneweaver.db.query.geneset.read import shared_with_user


def test_shared_with_user_raises_not_implemented():
    """Test that the shared_with_user function raises a NotImplementedError."""
    with pytest.raises(NotImplementedError):
        _ = shared_with_user(user_id=1)
