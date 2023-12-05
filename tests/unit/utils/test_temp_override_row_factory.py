"""Test the temp_override_row_factory decorator."""
from unittest.mock import Mock

import pytest
from geneweaver.db.utils import temp_override_row_factory


def test_temp_override_row_factory():
    """Test the temp_override_row_factory decorator."""
    # Define a mock cursor with a row_factory attribute
    mock_cursor = Mock()
    mock_cursor.row_factory = "original_factory"

    # Define a mock function to decorate
    @temp_override_row_factory("new_factory")
    def mock_function(cursor) -> None:
        return cursor.row_factory

    # Test if row_factory is temporarily overridden
    assert mock_function(mock_cursor) == "new_factory"
    # Test if original row_factory is restored
    assert mock_cursor.row_factory == "original_factory"


def test_temp_override_row_factory_with_exception():
    """Test the temp_override_row_factory decorator with an exception."""
    mock_cursor = Mock()
    mock_cursor.row_factory = "original_factory"

    @temp_override_row_factory("new_factory")
    def mock_function(cursor) -> None:
        raise Exception("test exception")

    # Test if original row_factory is restored even when an exception occurs
    with pytest.raises(Exception, match="test exception"):
        mock_function(mock_cursor)
    assert mock_cursor.row_factory == "original_factory"


def test_temp_override_row_factory_without_cursor():
    """Test the temp_override_row_factory decorator without providing a cursor."""

    @temp_override_row_factory("new_factory")
    def mock_function(cursor=None) -> None:
        """Mock function to test the decorator."""
        pass

    # Test if ValueError is raised when no cursor is provided
    with pytest.raises(ValueError, match="Cursor must be provided"):
        mock_function()
