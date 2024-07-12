"""Test the GeneWeaver Database module's settings class."""

from geneweaver.db.core.settings_class import Settings
from pydantic import BaseModel, PostgresDsn
from pydantic.networks import MultiHostUrl


class PostgresDsnExample(BaseModel):
    """Example of a PostgresDsn.

    Used to test that the postgres dsn string can be parsed.
    """

    db: PostgresDsn


def test_can_import_settings_class():
    """Test that we can import the settings class."""
    from geneweaver.db.core.settings_class import Settings as SettingsClassTest

    assert SettingsClassTest is not None
    assert SettingsClassTest is Settings


def test_settings_class_has_expected_attributes():
    """Test that the settings class has necessary attributes."""
    # Create a Settings instance
    settings = Settings(SERVER="localhost", USERNAME="admin", _env_file=None)

    # Check for attribute existence
    assert hasattr(settings, "SERVER"), "Missing attribute SERVER"
    assert hasattr(settings, "USERNAME"), "Missing attribute USER"
    assert hasattr(settings, "PASSWORD"), "Missing attribute PASSWORD"
    assert hasattr(settings, "NAME"), "Missing attribute NAME"
    assert hasattr(settings, "URI"), "Missing attribute URI"
    assert hasattr(settings, "PORT"), "Missing attribute PORT"

    # Check default values
    assert settings.PASSWORD == "", "Default for PASSWORD should be an empty string"
    assert settings.NAME == "", "Default for NAME should be an empty string"

    # Postgres uri should be parsable as PostgresDsn
    parsed = PostgresDsnExample(db=settings.URI)
    assert parsed is not None, "URI should be parsable as a PostgresDsn"
    assert parsed.db is not None, "URI should be parsable as a PostgresDsn"
    assert isinstance(
        parsed.db, MultiHostUrl
    ), "URI should be parsable as a PostgresDsn"

    # "localhost" should be replaced with 127.0.0.1
    assert (
        str(settings.URI) == "postgresql://admin@127.0.0.1:5432/"
    ), "URI not formatted as expected"

    # Check the non-default values
    # "localhost" should be replaced with 127.0.0.1
    assert settings.SERVER == "127.0.0.1", "Incorrect value for SERVER"
    assert settings.USERNAME == "admin", "Incorrect value for USER"


def test_settings_class_can_directly_set_database_uri():
    """Test that the settings class URI attribute can be directly set."""
    settings = Settings(
        SERVER="irrelevant",
        USERNAME="also_irrelevant",
        URI="postgresql://other_admin@non_localhost/",
        _env_file=None,
    )

    # Check for attribute existence
    assert hasattr(settings, "SERVER"), "Missing attribute SERVER"
    assert hasattr(settings, "USERNAME"), "Missing attribute USER"
    assert hasattr(settings, "PASSWORD"), "Missing attribute PASSWORD"
    assert hasattr(settings, "NAME"), "Missing attribute NAME"
    assert hasattr(settings, "URI"), "Missing attribute URI"

    # Check default values
    assert settings.PASSWORD == "", "Default for PASSWORD should be an empty string"
    assert settings.NAME == "", "Default for NAME should be an empty string"
    assert settings.PORT == 5432, "Default for PORT should be 5432"
    assert isinstance(settings.URI, str), "URI should be a string"

    # Postgres uri should be parsable as PostgresDsn
    parsed = PostgresDsnExample(db=settings.URI)
    assert parsed is not None, "URI should be parsable as a PostgresDsn"
    assert parsed.db is not None, "URI should be parsable as a PostgresDsn"
    assert isinstance(
        parsed.db, MultiHostUrl
    ), "URI should be parsable as a PostgresDsn"

    assert (
        str(settings.URI) == "postgresql://other_admin@non_localhost/"
    ), "URI not formatted as expected"

    # Check the non-default values
    assert settings.SERVER == "irrelevant", "Incorrect value for SERVER"
    assert settings.USERNAME == "also_irrelevant", "Incorrect value for USER"


def test_settings_from_env(monkeypatch):
    """Test the settings class can be configured from environment variables."""
    # Set the environment variables
    monkeypatch.setenv("GWDB_SERVER", "localhost")
    monkeypatch.setenv("GWDB_USERNAME", "admin")
    monkeypatch.setenv("GWDB_PASSWORD", "secret")
    monkeypatch.setenv("GWDB_NAME", "database")

    # Create a Settings instance
    settings = Settings(_env_file=None)

    # Check if environment variables were correctly set

    # localhost should be replaced by 127.0.0.1
    assert settings.SERVER == "127.0.0.1", "Incorrect value for SERVER"
    assert settings.USERNAME == "admin", "Incorrect value for USER"
    assert settings.PASSWORD == "secret", "Incorrect value for PASSWORD"
    assert settings.NAME == "database", "Incorrect value for NAME"
