"""API tests."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    "payload,expected_status_code,expected_response",
    [
        (
            {
                "userKey": "foo",
                "deviceType": "Android",
            },
            status.HTTP_200_OK,
            {"statusCode": 200},
        ),
        (
            {
                "user_key": "foo",
                "device_type": "iOS",
            },
            status.HTTP_400_BAD_REQUEST,
            {"statusCode": 400},
        ),
        (
            {
                "userKey": "foo",
                "deviceType": "bar",
            },
            status.HTTP_400_BAD_REQUEST,
            {"statusCode": 400},
        ),
    ],
)
def test_api_endpoint_register_device_event(
    mocker: MockerFixture,
    device_registration_fast_api_test_client: TestClient,
    payload: dict[str, str],
    expected_status_code: int,
    expected_response: dict[str, str],
) -> None:
    """Test API endpoint register device event.

    :param mocker:
    :param device_registration_fast_api_test_client:
    :param payload:
    :param expected_status_code:
    :param expected_response:
    :return:
    """
    mocked_background_task_call = mocker.patch(
        "app.device_registration.api.v1.endpoints.create_device_registration_event"
    )
    response = device_registration_fast_api_test_client.post(
        "/device-registration/v1/Device/register", json=payload
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_response
    if response.status_code == status.HTTP_200_OK:
        mocked_background_task_call.assert_called_once()
    else:
        mocked_background_task_call.assert_not_called()
