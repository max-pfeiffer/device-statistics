"""Test fixtures."""

from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient


@pytest.fixture
def device_registration_environment() -> None:
    """Device registration environment variables.

    :return:
    """
    env_file_path = (
        Path(__file__).parent.parent.resolve()
        / "config"
        / "device-registrations-app.env"
    )
    load_dotenv(env_file_path)


@pytest.fixture
def device_registration_fast_api_test_client(
    device_registration_environment,
) -> TestClient:
    """Test client for device registration app.

    :param device_registration_environment:
    :return:
    """
    from app.device_registration.main import app

    return TestClient(app)
