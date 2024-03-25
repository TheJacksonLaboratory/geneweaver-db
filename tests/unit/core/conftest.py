"""Fixtures for the core module unit tests."""

import pytest


@pytest.fixture()
def _monkeypatch_settings_env(monkeypatch) -> None:
    """Monkeypatch the environment variables used by the settings.config module."""
    monkeypatch.setenv("GWDB_USERNAME", "test_username")
    monkeypatch.setenv("GWDB_PASSWORD", "test_password")
    monkeypatch.setenv("GWDB_NAME", "test_db_name")
    monkeypatch.setenv("GWDB_SERVER", "test_host")
