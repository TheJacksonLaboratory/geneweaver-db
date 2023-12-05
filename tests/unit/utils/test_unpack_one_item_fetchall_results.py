"""Test the unpack_one_item_fetchall_results function."""
import pytest
from geneweaver.db.exceptions import GeneweaverDoesNotExistError, GeneweaverValueError
from geneweaver.db.utils import unpack_one_item_fetchall_results


def test_empty_results():
    """An error is raised when no results are found."""
    with pytest.raises(GeneweaverDoesNotExistError, match="No results found."):
        unpack_one_item_fetchall_results([])


def test_single_row_single_column():
    """The function correctly unpacks a single row with a single column."""
    results = [("value1",)]
    assert unpack_one_item_fetchall_results(results) == ["value1"]


def test_multiple_rows_single_column():
    """The function correctly unpacks multiple rows with a single column each."""
    results = [("value1",), ("value2",), ("value3",)]
    assert unpack_one_item_fetchall_results(results) == ["value1", "value2", "value3"]


def test_single_row_multiple_columns():
    """An error is raised when there are too many columns to unpack."""
    with pytest.raises(GeneweaverValueError, match="Too many results to unpack."):
        unpack_one_item_fetchall_results([("value1", "value2")])
