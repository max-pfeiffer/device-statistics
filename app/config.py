"""Application configuration."""

import semver
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class ApplicationSettings(BaseSettings):
    """Application settings."""

    title: str = "Device Statistics"
    description: str = "REST API for device statistics."
    version: str = "0.1.0"

    @computed_field
    def api_prefix(self) -> str:
        """Return API prefix.

        :return:
        """
        version = semver.Version.parse(self.version)
        return f"/v{version.major}"


class DatabaseSettings(BaseSettings):
    """Database settings."""

    user: str
    password: str
    name: str
    rollback: bool = False
    host: str
    port: str = "5432"

    @computed_field
    def database_url(self) -> str:
        """URI for Postgresql database connection.

        :return:
        """
        url_object = URL.create(
            "postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.name,
        )
        return url_object.render_as_string()

    model_config = SettingsConfigDict(env_prefix="DATABASE_", env_file=".env")


application_settings = ApplicationSettings()
database_settings = DatabaseSettings()
