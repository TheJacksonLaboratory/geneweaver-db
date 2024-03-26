"""Test the async convenience cursor context manager."""

from unittest.mock import MagicMock, patch

import pytest
from psycopg.cursor_async import AsyncCursor


@patch("geneweaver.db.core.cursor.settings.URI", "test_uri")
@patch("geneweaver.db.core.cursor.psycopg.AsyncConnection.connect")
@pytest.mark.usefixtures("_monkeypatch_settings_env")
async def test_async_cursor(mock_connect):
    """Test the cursor context manager."""
    from geneweaver.db.core.cursor import async_cursor

    mock_connection = MagicMock()
    mock_cursor = MagicMock(spec=AsyncCursor)
    mock_connect.return_value.__aenter__.return_value = mock_connection
    mock_connection.cursor.return_value.__aenter__.return_value = mock_cursor

    async with async_cursor() as cursor_:
        assert mock_cursor == cursor_

    assert mock_connect.called is True
    assert mock_connect.call_args[0][0] == "test_uri"

    assert mock_connection.cursor.called is True
    assert mock_connection.cursor.call_args[0] == ()
