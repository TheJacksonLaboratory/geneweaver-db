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
from typing import Optional

from pydantic import PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for the GeneWeaver Database module."""

    DEBUG_MODE = False

    CONNECTION_SCHEME: str = "postgresql"

    SERVER: str
    USERNAME: str
    PASSWORD: str = ""
    NAME: str = ""
    PORT: int = 5432
    URI: Optional[str] = None

    @field_validator("SERVER", mode="after")
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if v == "localhost":
            return "127.0.0.1"
        return v

    @model_validator(mode="after")
    def assemble_db_connection(self):
        if isinstance(self.URI, str):
            self.URI = str(PostgresDsn(self.URI))
        else:
            self.URI = str(
                PostgresDsn.build(
                    scheme=self.CONNECTION_SCHEME,
                    user=self.USERNAME,
                    password=self.PASSWORD,
                    host=self.SERVER,
                    port=str(self.PORT),
                    path=f"/{self.NAME or ''}",
                )
            )

    model_config = SettingsConfigDict(
        env_prefix="GWDB_", env_file=".env", case_sensitive=True
    )
