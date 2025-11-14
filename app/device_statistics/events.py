"""Device registration events."""

from furl import furl
from httpx import post
from sqlmodel import Session

from app.core.repositories import DeviceRegistrationsRepository
from app.device_statistics.config import statistics_application_settings


def user_login_command(user_key: str, device_type: str) -> None:
    """User login command.

    :param user_key:
    :param device_type:
    :return:
    """
    furl_item: furl = furl(
        statistics_application_settings.api_device_registration_base_url
    )
    furl_item.path /= (
        statistics_application_settings.api_device_registration_path_device_register
    )

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
