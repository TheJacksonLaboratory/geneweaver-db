"""The settings class definition for the GeneWeaver Database module.

This class is intended to be used with environment variables, and will attempt to
load them from a `.env` file in the root of the project. The following environment
variables are used:
GWDB_SERVER=your_server
GWDB_USER=your_user
GWDB_PASSWORD=your_password
GWDB_NAME=your_database_name
"""
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Settings class for the GeneWeaver Database module."""

    SERVER: str
    USER: str
    PASSWORD: str = ""
    NAME: str = ""
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("USER"),
            password=values.get("PASSWORD"),
            host=values.get("SERVER"),
            path=f"/{values.get('NAME') or ''}",
        )

    class Config:
        env_prefix = "GWDB_"
        env_file = ".env"
        case_sensitive = True
