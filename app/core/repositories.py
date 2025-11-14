"""Repositories."""

from datetime import datetime

from sqlalchemy.exc import NoResultFound
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

    def create_or_update_device_registrations(
        self, user_key: str, device_type: str
    ) -> None:
        """Create or update device registrations.

        A user can have multiple devices i.e., an Android mobile device and a TV.
        Therefore, we first check if a device of that type was already registered
        for that user key. If not, we create a new row with the new device type.

        :param user_key:
        :param device_type:
        :return:
        """
        statement = (
            select(UserDeviceType)
            .where(UserDeviceType.user_key == user_key)
            .where(UserDeviceType.device_type == device_type)
        )
        try:
            self.session.exec(statement).one()
        except NoResultFound:
            new_user_device_type = UserDeviceType(
                user_key=user_key, device_type=device_type, created_at=datetime.now()
            )
            self.session.add(new_user_device_type)
