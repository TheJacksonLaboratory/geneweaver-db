"""Test the geneset.core.settings.config Settings instance."""


def test_is_importable_and_initialized(monkeypatch_settings_env):
    """Test that the settings.config Settings instance is importable and initialized."""
    from geneweaver.db.core.settings import Settings, settings

    assert settings is not None
    assert isinstance(settings, Settings)
