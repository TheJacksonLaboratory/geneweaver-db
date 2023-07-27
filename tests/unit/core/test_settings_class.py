"""Test the GeneWeaver Database module's settings class."""
from geneweaver.db.core.settings_class import Settings
from pydantic import PostgresDsn


def test_can_import_settings_class():
    """Test that we can import the settings class."""
    from geneweaver.db.core.settings_class import Settings as SettingsClassTest

    assert SettingsClassTest is not None
    assert SettingsClassTest is Settings


def test_settings_class_has_expected_attributes():
    """Test that the settings class has necessary attributes."""
    # Create a Settings instance
    settings = Settings(SERVER="localhost", USER="admin")

    # Check for attribute existence
    assert hasattr(settings, "SERVER"), "Missing attribute SERVER"
    assert hasattr(settings, "USER"), "Missing attribute USER"
    assert hasattr(settings, "PASSWORD"), "Missing attribute PASSWORD"
    assert hasattr(settings, "NAME"), "Missing attribute NAME"
    assert hasattr(settings, "DATABASE_URI"), "Missing attribute DATABASE_URI"

    # Check default values
    assert settings.PASSWORD == "", "Default for PASSWORD should be an empty string"
    assert settings.NAME == "", "Default for NAME should be an empty string"
    assert isinstance(
        settings.DATABASE_URI, PostgresDsn
    ), "DATABASE_URI should be a PostgresDsn"

    assert (
        str(settings.DATABASE_URI) == "postgresql://admin@localhost/"
    ), "DATABASE_URI not formatted as expected"

    # Check the non-default values
    assert settings.SERVER == "localhost", "Incorrect value for SERVER"
    assert settings.USER == "admin", "Incorrect value for USER"


def test_settings_class_can_directly_set_database_uri():
    """Test that the settings class DATABASE_URI attribute can be directly set."""
    settings = Settings(
        SERVER="irrelevant",
        USER="also_irrelevant",
        DATABASE_URI="postgresql://other_admin@non_localhost/",
    )

    # Check for attribute existence
    assert hasattr(settings, "SERVER"), "Missing attribute SERVER"
    assert hasattr(settings, "USER"), "Missing attribute USER"
    assert hasattr(settings, "PASSWORD"), "Missing attribute PASSWORD"
    assert hasattr(settings, "NAME"), "Missing attribute NAME"
    assert hasattr(settings, "DATABASE_URI"), "Missing attribute DATABASE_URI"

    # Check default values
    assert settings.PASSWORD == "", "Default for PASSWORD should be an empty string"
    assert settings.NAME == "", "Default for NAME should be an empty string"
    assert isinstance(
        settings.DATABASE_URI, PostgresDsn
    ), "DATABASE_URI should be a PostgresDsn"

    assert (
        str(settings.DATABASE_URI) == "postgresql://other_admin@non_localhost/"
    ), "DATABASE_URI not formatted as expected"

    # Check the non-default values
    assert settings.SERVER == "irrelevant", "Incorrect value for SERVER"
    assert settings.USER == "also_irrelevant", "Incorrect value for USER"


def test_settings_from_env(monkeypatch):
    """Test the settings class can be configured from environment variables."""
    # Set the environment variables
    monkeypatch.setenv("GWDB_SERVER", "localhost")
    monkeypatch.setenv("GWDB_USER", "admin")
    monkeypatch.setenv("GWDB_PASSWORD", "secret")
    monkeypatch.setenv("GWDB_NAME", "database")

    # Create a Settings instance
    settings = Settings()

    # Check if environment variables were correctly set
    assert settings.SERVER == "localhost", "Incorrect value for SERVER"
    assert settings.USER == "admin", "Incorrect value for USER"
    assert settings.PASSWORD == "secret", "Incorrect value for PASSWORD"
    assert settings.NAME == "database", "Incorrect value for NAME"
