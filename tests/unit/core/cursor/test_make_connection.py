"""Test the make_connection convenience function."""

from unittest.mock import MagicMock, patch

from geneweaver.db.core.cursor import make_connection


@patch("geneweaver.db.core.cursor.psycopg.connect")
@patch("geneweaver.db.core.settings_class.Settings", MagicMock)
@patch("geneweaver.db.core.cursor.settings.URI", "test_uri")
def test_make_connection(mock_connect):
    """Test the make_connection function."""
    mock_connect.return_value = "test_connection"

    connection = make_connection()

    assert mock_connect.called is True
    assert mock_connect.call_args[0][0] == "test_uri"
    assert connection == "test_connection"
