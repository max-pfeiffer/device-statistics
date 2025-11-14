"""Device registration events."""

from furl import furl
from httpx import post
from sqlmodel import Session

from core.repositories import DeviceRegistrationsRepository
from device_registration.config import application_settings


def user_login_command(user_key: str, device_type: str) -> None:
    """User login command.

    :param user_key:
    :param device_type:
    :return:
    """
    furl_item: furl = furl(application_settings.api_statistics_base_url)
    furl_item.path /= application_settings.api_statistics_path_device_registrations

    payload = {
        "userKey": user_key,
        "deviceType": device_type,
    }

    response = post(furl_item.url, json=payload)
    response.raise_for_status()


def device_registrations_query(device_type: str, database_session: Session) -> int:
    """Query for device registrations.

    :param device_type:
    :param database_session:
    :return:
    """
    with database_session.begin():
        repo = DeviceRegistrationsRepository(database_session)
        count = repo.get_device_type_count(device_type)

    if count == 0:
        return -1
    else:
        return count
