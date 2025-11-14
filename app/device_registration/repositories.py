"""Repositories."""

from sqlmodel import Session, col, func, select

from app.database.models import UserDeviceType


class DeviceRegistrationsRepository:
    """DeviceRegistrationsRepository."""

    def __init__(self, session: Session) -> None:
        """Initialize object.

        :param Session session:
        """
        self.session: Session = session

    def get_device_type_count(self, device_type: str) -> int:
        """Get the number of devices registered.

        :param kwargs:
        :return:
        """
        statement = select(func.count(col(UserDeviceType.id))).where(
            UserDeviceType.device_type == device_type
        )
        count = self.session.exec(statement).one()
        return count
