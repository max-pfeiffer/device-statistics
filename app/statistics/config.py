"""Application configuration."""

import semver
from pydantic import computed_field
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """Application settings."""

    title: str = "Statistics"
    description: str = "REST API for statistics."
    version: str = "1.0.0"

    @computed_field
    def api_prefix(self) -> str:
        """Return API prefix.

        :return:
        """
        version = semver.Version.parse(self.version)
        return f"/v{version.major}"


application_settings = ApplicationSettings()
