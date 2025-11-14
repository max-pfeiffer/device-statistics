"""Application configuration."""

import semver
from pydantic import computed_field
from pydantic_settings import BaseSettings


class StatisticsApplicationSettings(BaseSettings):
    """Application settings."""

    title: str = "Statistics"
    description: str = "REST API for statistics."
    version: str = "1.0.0"
    api_device_registration_base_url: str = (
        "http://localhost:9000/device-registration/v1"
    )
    api_device_registration_path_device_register: str = "Device/register"

    @computed_field
    def api_prefix(self) -> str:
        """Return API prefix.

        :return:
        """
        version = semver.Version.parse(self.version)
        return f"/v{version.major}"


statistics_application_settings = StatisticsApplicationSettings()
