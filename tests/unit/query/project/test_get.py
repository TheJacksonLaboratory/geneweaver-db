"""Test the project.get query generation function."""

import pytest
from geneweaver.db.query.project import PROJECT_FIELD_MAP, get


@pytest.mark.parametrize("project_id", [None, 12345])
@pytest.mark.parametrize("owner_id", [None, 47])
@pytest.mark.parametrize("name", [None, "test"])
@pytest.mark.parametrize("starred", [None, True, False])
@pytest.mark.parametrize("search_text", [None, "search text test"])
@pytest.mark.parametrize("limit", [None, 1, 10])
@pytest.mark.parametrize("offset", [None, 1, 10])
def test_all_kwargs(project_id, owner_id, name, starred, search_text, limit, offset):
    """Test all the kwarg combinations for query.gene.get."""
    query, params = get(
        project_id=project_id,
        owner_id=owner_id,
        name=name,
        starred=starred,
        search_text=search_text,
        limit=limit,
        offset=offset,
    )

    if project_id is not None:
        assert "id" in params
    else:
        assert "id" not in params

    if owner_id is not None:
        assert "usr_id" in params
    else:
        assert "usr_id" not in params

    if name is not None:
        assert "name" in params
    else:
        assert "name" not in params

    if starred is not None:
        assert "star" in params
    else:
        assert "star" not in params

    str_query = str(query)

    for key, value in PROJECT_FIELD_MAP.items():
        assert value in str_query
        assert key in str_query
