"""Test the limit_an_offset query generation utility function."""

import pytest
from geneweaver.db.utils import limit_and_offset
from psycopg.sql import SQL


@pytest.mark.parametrize("limit", [None, 10, 100, 2000, 45678])
@pytest.mark.parametrize("offset", [None, 10, 100, 2000, 45678])
def test_limit_and_offest(limit, offset):
    """Test the limit_and_offset query generation utility function."""
    q = (SQL("SELECT *") + SQL("FROM table")).join(" ")
    result = limit_and_offset(q, limit, offset)
    if limit is not None:
        assert str(limit) in str(result)
    else:
        assert str(limit) not in str(result)

    if offset is not None:
        assert str(offset) in str(result)
    else:
        assert str(offset) not in str(result)
