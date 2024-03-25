"""Test the geneset.core.settings.config Settings instance."""

import pytest


@pytest.mark.usefixtures("_monkeypatch_settings_env")
def test_is_importable_and_initialized():
    """Test that the settings.config Settings instance is importable and initialized."""
    from geneweaver.db.core.settings import Settings, settings

    assert settings is not None
    assert isinstance(settings, Settings)
