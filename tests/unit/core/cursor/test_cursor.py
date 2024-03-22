"""Test the convenience cursor context manager."""

from unittest.mock import MagicMock, patch


@patch("geneweaver.db.core.cursor.settings.URI", "test_uri")
@patch("geneweaver.db.core.cursor.psycopg.connect")
@patch("geneweaver.db.core.settings_class.Settings", MagicMock())
def test_cursor(mock_connect):
    """Test the cursor context manager."""
    from geneweaver.db.core.cursor import cursor

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    with cursor() as cursor_:
        assert mock_cursor == cursor_

    assert mock_connect.called is True
    assert mock_connect.call_args[0][0] == "test_uri"

    assert mock_connection.cursor.called is True
    assert mock_connection.cursor.call_args[0] == ()
