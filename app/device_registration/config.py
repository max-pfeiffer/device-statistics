"""Application configuration."""

import semver
from pydantic import computed_field
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """Application settings."""

    title: str = "Device Registration"
    description: str = "REST API for device registrations."
    version: str = "1.0.0"

    @computed_field
    def api_prefix(self) -> str:
        """Return API prefix.

        :return:
        """
        version = semver.Version.parse(self.version)
        return f"/v{version.major}"


application_settings = ApplicationSettings()
