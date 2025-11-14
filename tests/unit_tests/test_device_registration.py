"""Unit tests for device registration app."""

from unittest.mock import MagicMock

import pytest
from app.core.enums import DeviceType
from app.device_registration.events import device_registrations_query
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "payload,expected_status_code,expected_response",
    [
        (
            {
                "userKey": "foo",
                "deviceType": "Android",
            },
            status.HTTP_200_OK,
            {"statusCode": 200, "message": "success"},
        ),
        (
            {
                "user_key": "foo",
                "device_type": "iOS",
            },
            status.HTTP_400_BAD_REQUEST,
            {"statusCode": 400, "message": "bad_request"},
        ),
        (
            {
                "userKey": "foo",
                "deviceType": "bar",
            },
            status.HTTP_400_BAD_REQUEST,
            {"statusCode": 400, "message": "bad_request"},
        ),
    ],
)
def test_api_endpoint_create_user_login_event(
    mocker,
    device_registration_fast_api_test_client: TestClient,
    payload: dict[str, str],
    expected_status_code: int,
    expected_response: dict[str, str],
) -> None:
    """Test API endpoint create user login event.

    :param mocker:
    :param device_registration_fast_api_test_client:
    :param payload:
    :param expected_status_code:
    :param expected_response:
    :return:
    """
    mocked_background_task_call = mocker.patch(
        "app.device_registration.api.v1.endpoints.BackgroundTasks.add_task"
    )
    response = device_registration_fast_api_test_client.post(
        "/device_registration/v1/Log/auth", json=payload
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_response
    if response.status_code == status.HTTP_200_OK:
        mocked_background_task_call.assert_called_once()
    else:
        mocked_background_task_call.assert_not_called()


@pytest.mark.parametrize(
    "params,expected_status_code,expected_response",
    [
        (
            {
                "deviceType": "Android",
            },
            status.HTTP_200_OK,
            {"deviceType": "Android", "count": 10},
        ),
        (
            {
                "device_type": "bar",
            },
            status.HTTP_400_BAD_REQUEST,
            {"statusCode": 400, "message": "bad_request"},
        ),
        (
            {
                "deviceType": "bar",
            },
            status.HTTP_400_BAD_REQUEST,
            {"statusCode": 400, "message": "bad_request"},
        ),
    ],
)
def test_api_endpoint_get_device_registrations(
    mocker,
    device_registration_fast_api_test_client: TestClient,
    params: dict[str, str],
    expected_status_code: int,
    expected_response: dict[str, str],
) -> None:
    """Test API endpoint for get device registrations.

    :param mocker:
    :param device_registration_fast_api_test_client:
    :param params:
    :param expected_status_code:
    :param expected_response:
    :return:
    """
    mocked_device_registrations_query = mocker.patch(
        "app.device_registration.api.v1.endpoints.events.device_registrations_query",
        return_value=10,
    )
    response = device_registration_fast_api_test_client.get(
        "/device_registration/v1/Log/auth/statistics", params=params
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_response
    if response.status_code == status.HTTP_200_OK:
        mocked_device_registrations_query.assert_called_once()
    else:
        mocked_device_registrations_query.assert_not_called()


@pytest.mark.parametrize("repo_result, expected_result", [(15, 15), (0, -1)])
def test_device_registrations_query(mocker, repo_result, expected_result) -> None:
    """Test device registrations query event.

    :param mocker:
    :param repo_result:
    :param expected_result:
    :return:
    """
    mocked_get_device_type_count = mocker.patch(
        "app.device_registration.events.DeviceRegistrationsRepository.get_device_type_count",
        return_value=repo_result,
    )

    result = device_registrations_query(DeviceType.ANDROID.value, MagicMock())
    assert result == expected_result
    mocked_get_device_type_count.assert_called_once()
