"""The settings class definition for the GeneWeaver Database module.

This class is intended to be used with environment variables, and will attempt to
load them from a `.env` file in the root of the project. The following environment
variables are used:
GWDB_SERVER=your_server
GWDB_USERNAME=your_user
GWDB_PASSWORD=your_password
GWDB_NAME=your_database_name
"""
# ruff: noqa: N805, ANN101, ANN401
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Settings class for the GeneWeaver Database module."""

    DEBUG_MODE = False

    SERVER: str
    USERNAME: str
    PASSWORD: str = ""
    NAME: str = ""
    PORT: int = 5432
    URI: Optional[str] = None

    @validator("SERVER", pre=True)
    def replace_localhost(cls, v: str) -> str:
        """Replace localhost with 127.0.0.1."""
        if v == "localhost":
            return "127.0.0.1"
        return v

    @validator("URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Build the database connection string, unless one is provided."""
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                user=values.get("USERNAME"),
                password=values.get("PASSWORD"),
                host=values.get("SERVER"),
                port=str(values.get("PORT")),
                path=f"/{values.get('NAME') or ''}",
            )
        )

    class Config:
        """Configuration for the BaseSettings class."""

        env_prefix = "GWDB_"
        env_file = ".env"
        case_sensitive = True
