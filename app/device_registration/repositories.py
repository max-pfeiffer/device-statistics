"""Repositories."""

from sqlmodel import Session


class DeviceRegistrationsRepository:
    """DeviceRegistrationsRepository."""

    def __init__(self, session: Session) -> None:
        """Initialize object.

        :param Session session:
        """
        self.session: Session = session

    def get_device_type_amount(self, device_type: str) -> int:
        """Get the number of devices registered.

        :param kwargs:
        :return:
        """
        pass
