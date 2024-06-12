"""Test the project.shared_with_user query generation function."""

import pytest
from geneweaver.db.query.project import PROJECT_FIELD_MAP, shared_with_user


@pytest.mark.parametrize("usr_id", [47])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
def test_all_kwargs(usr_id, limit, offset):
    """Test all the kwarg combinations for query.project.shared_with_user."""
    query, params = shared_with_user(
        user_id=usr_id,
        limit=limit,
        offset=offset,
    )

    assert "user_id" in params

    str_query = str(query)

    for key, value in PROJECT_FIELD_MAP.items():
        assert value in str_query
        assert key in str_query

    assert "owner" in str_query
