"""Test the project.get query generation function."""


import pytest
from geneweaver.db.query.project import get


def test_get_raise_not_implemented():
    with pytest.raises(NotImplementedError):
        _ = get(
            project_id=1,
            owner_id=1,
            name='test',
            starred=True,
            search_text='search',
            limit=1,
            offset=10,
        )
