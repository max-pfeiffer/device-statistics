"""Test fixtures."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def device_statistics_environment(monkeypatch) -> None:
    """Set up device registration environment variables.

    :return:
    """
    monkeypatch.setenv("DATABASE_USER", "testuser")
    monkeypatch.setenv("DATABASE_PASSWORD", "supersecret")
    monkeypatch.setenv("DATABASE_NAME", "devicestatistics")
    monkeypatch.setenv("DATABASE_USER", "testuser")
    monkeypatch.setenv("DATABASE_ROLLBACK", "false")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PORT", "5432")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PORT", "5432")
    monkeypatch.setenv(
        "API_DEVICE_REGISTRATION_BASE_URL",
        "http://localhost:9000/device-registration/v1",
    )
    monkeypatch.setenv(
        "API_DEVICE_REGISTRATION_PATH_DEVICE_REGISTER", "Device/register"
    )


@pytest.fixture
def device_statistics_fast_api_test_client(
    device_statistics_environment,
) -> TestClient:
    """Test client for device registration app.

    :param device_registration_environment:
    :return:
    """
    from app.device_statistics.main import app

    return TestClient(app)
