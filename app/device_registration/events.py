"""Device registration events."""

from sqlmodel import Session

from app.device_registration.repositories import DeviceRegistrationsRepository


def user_login_command(user_key: str, device_type: str) -> None:
    """User login command.

    :param user_key:
    :param device_type:
    :return:
    """
    pass


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
