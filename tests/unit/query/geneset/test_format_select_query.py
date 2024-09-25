"""Test the format_select_query sql generation function."""

# ruff: noqa: C901
import pytest
from geneweaver.db.query.const import PUB_FIELD_MAP
from geneweaver.db.query.geneset.const import GENESET_FIELDS_MAP
from geneweaver.db.query.geneset.utils import format_select_query


@pytest.mark.parametrize("with_publication_info", [None, True, False])
@pytest.mark.parametrize("with_publication_join", [None, True, False])
def test_format_select_query(with_publication_info, with_publication_join):
    """Test the format_select_query sql generation function."""
    kwargs = {}
    if with_publication_info is not None:
        kwargs["with_publication_info"] = with_publication_info
    if with_publication_join is not None:
        kwargs["with_publication_join"] = with_publication_join

    result = format_select_query(**kwargs)
    str_results = str(result)
    assert "SELECT" in str_results
    assert "FROM geneset" in str_results

    for field in GENESET_FIELDS_MAP.keys():
        assert field in str_results

    if with_publication_info is True:
        for field in PUB_FIELD_MAP.keys():
            assert field in str_results

    if with_publication_join is True or with_publication_info is True:
        assert "JOIN publication" in str_results
        assert "LEFT OUTER JOIN" in str_results
        assert "ON geneset.pub_id = publication.pub_id" in str_results

    if with_publication_join is True and with_publication_info is False:
        for field in PUB_FIELD_MAP.keys():
            if field != "pub_id":
                assert field not in str_results

    if with_publication_join is False and with_publication_info is False:
        for field in PUB_FIELD_MAP.keys():
            if field != "pub_id":
                assert field not in str_results
        assert "JOIN publication" not in str_results
        assert "LEFT OUTER JOIN" not in str_results
