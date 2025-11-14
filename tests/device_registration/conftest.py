"""Test fixtures."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def device_registration_environment(monkeypatch) -> None:
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
