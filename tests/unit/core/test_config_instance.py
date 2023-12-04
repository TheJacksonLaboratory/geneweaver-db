"""Test the geneset.core.settings.config Settings instance."""


def test_is_importable_and_initialized(monkeypatch):
    """Test that the settings.config Settings instance is importable and initialized."""
    monkeypatch.setenv("GWDB_USERNAME", "test_username")
    monkeypatch.setenv("GWDB_PASSWORD", "test_password")
    monkeypatch.setenv("GWDB_NAME", "test_db_name")
    monkeypatch.setenv("GWDB_SERVER", "test_host")

    from geneweaver.db.core.settings import Settings, config

    assert config is not None
    assert isinstance(config, Settings)
