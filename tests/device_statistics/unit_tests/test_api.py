"""Unit tests for device registration app."""

import pytest
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
    device_statistics_fast_api_test_client: TestClient,
    payload: dict[str, str],
    expected_status_code: int,
    expected_response: dict[str, str],
    jwt_string: str,
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
        "app.device_statistics.api.v1.endpoints.BackgroundTasks.add_task"
    )
    headers = {
        "Authorization": f"Bearer {jwt_string}",
    }

    response = device_statistics_fast_api_test_client.post(
        "/device-statistics/v1/Log/auth", json=payload, headers=headers
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
    device_statistics_fast_api_test_client: TestClient,
    params: dict[str, str],
    expected_status_code: int,
    expected_response: dict[str, str],
    jwt_string: str,
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
        "app.device_statistics.api.v1.endpoints.events.device_registrations_query",
        return_value=10,
    )
    headers = {
        "Authorization": f"Bearer {jwt_string}",
    }

    response = device_statistics_fast_api_test_client.get(
        "/device-statistics/v1/Log/auth/statistics", params=params, headers=headers
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_response
    if response.status_code == status.HTTP_200_OK:
        mocked_device_registrations_query.assert_called_once()
    else:
        mocked_device_registrations_query.assert_not_called()
