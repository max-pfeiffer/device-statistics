"""Device registration events."""

from sqlmodel import Session

from device_registration.repositories import DeviceRegistrationsRepository


def user_login_command(user_key: str, device_type: str) -> None:
    """User login command.

    :param user_key:
    :param device_type:
    :return:
    """
    pass


def device_registrations_query(
    device_type: str, database_session: Session
) -> tuple[str, int]:
    """Device registrations query.

    :param device_type:
    """
    repo = DeviceRegistrationsRepository(database_session)
    amount = repo.get_device_type_amount(device_type)
    return device_type, amount
