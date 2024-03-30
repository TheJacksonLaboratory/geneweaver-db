"""Test the project.shared_with_user query generation function."""


import pytest
from geneweaver.db.query.project import shared_with_user


def test_shared_with_user_raise_not_implemented():
    with pytest.raises(NotImplementedError):
        _ = shared_with_user(
            user_id=1,
            limit=1,
            offset=10,
        )
