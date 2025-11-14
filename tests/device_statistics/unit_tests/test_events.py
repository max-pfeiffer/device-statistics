"""Tests for events."""

from unittest.mock import MagicMock

import pytest
from app.core.enums import DeviceType
from app.device_statistics.events import device_registrations_query


@pytest.mark.parametrize("repo_result, expected_result", [(15, 15), (0, -1)])
def test_device_registrations_query(mocker, repo_result, expected_result) -> None:
    """Test device registrations query event.

    :param mocker:
    :param repo_result:
    :param expected_result:
    :return:
    """
    mocked_get_device_type_count = mocker.patch(
        "app.device_statistics.events.DeviceRegistrationsRepository.get_device_type_count",
        return_value=repo_result,
    )

    result = device_registrations_query(DeviceType.ANDROID.value, MagicMock())
    assert result == expected_result
    mocked_get_device_type_count.assert_called_once()
