"""Test fixtures."""

import pytest
from authlib.jose import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

IDP_ISS = "https://auth.test.com"


@pytest.fixture(scope="session")
def rsa_keys() -> tuple[str, str]:
    """RSA keys fixture.

    :return:
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_pem_string = private_pem.decode("utf-8")
    public_pem_string = public_pem.decode("utf-8")
    return private_pem_string, public_pem_string


@pytest.fixture
def device_statistics_environment(monkeypatch, rsa_keys: tuple[str, str]) -> None:
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
    monkeypatch.setenv("IDP_PUBLIC_KEY", rsa_keys[1])
    monkeypatch.setenv("IDP_ISS", IDP_ISS)


@pytest.fixture
def device_statistics_fast_api_test_client(
    device_statistics_environment,
) -> TestClient:
    """Test client for device registration app.

    :param device_registration_environment:
    :return:
    """
    # Import settings to make the application ingest the environment variables
    from app.device_statistics.main import app

    return TestClient(app)


@pytest.fixture
def jwt_string(rsa_keys: tuple[str, str]) -> str:
    """JWT fixture.

    :param rsa_keys:
    :return:
    """
    private_key = rsa_keys[0]

    header = {"alg": "RS256"}
    payload = {"iss": IDP_ISS, "scope": ["login", "statistics"]}

    token_bytes = jwt.encode(header, payload, private_key)
    token_string = token_bytes.decode("utf-8")
    return token_string


@pytest.fixture
def jwt_string_login_scope(rsa_keys: tuple[str, str]) -> str:
    """JWT fixture.

    :param rsa_keys:
    :return:
    """
    private_key = rsa_keys[0]

    header = {"alg": "RS256"}
    payload = {"iss": IDP_ISS, "scope": ["login"]}

    token_bytes = jwt.encode(header, payload, private_key)
    token_string = token_bytes.decode("utf-8")
    return token_string


@pytest.fixture
def jwt_string_statistics_scope(rsa_keys: tuple[str, str]) -> str:
    """JWT fixture.

    :param rsa_keys:
    :return:
    """
    private_key = rsa_keys[0]

    header = {"alg": "RS256"}
    payload = {"iss": IDP_ISS, "scope": ["statistics"]}

    token_bytes = jwt.encode(header, payload, private_key)
    token_string = token_bytes.decode("utf-8")
    return token_string
