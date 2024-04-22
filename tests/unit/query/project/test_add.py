"""Test the project.add query generation function."""

import pytest
from geneweaver.db.query.project import add


def test_add_raise_not_implemented():
    """Test that the add function raises a NotImplementedError."""
    with pytest.raises(NotImplementedError):
        _ = add(user_id=1, name="test", notes="notes", starred=True)
