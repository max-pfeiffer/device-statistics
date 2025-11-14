"""Events."""

from sqlmodel import Session

from app.core.repositories import DeviceRegistrationsRepository


def create_device_registration_event(
    user_key: str, device_type: str, database_session: Session
) -> None:
    """Device registration event.

    :param user_key:
    :param device_type:
    :param database_session:
    :return:
    """
    with database_session.begin():
        repo = DeviceRegistrationsRepository(database_session)
        repo.create_or_update_device_registrations(user_key, device_type)
