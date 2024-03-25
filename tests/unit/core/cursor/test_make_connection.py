"""Test the make_connection convenience function."""

from unittest.mock import patch


@patch("geneweaver.db.core.cursor.settings.URI", "test_uri")
@patch("geneweaver.db.core.cursor.psycopg.connect")
def test_make_connection(mock_connect, monkeypatch_settings_env):
    """Test the make_connection function."""
    from geneweaver.db.core.cursor import make_connection

    mock_connect.return_value = "test_connection"

    connection = make_connection()

    assert mock_connect.called is True
    assert mock_connect.call_args[0][0] == "test_uri"
    assert connection == "test_connection"
