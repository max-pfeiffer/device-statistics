"""API endpoints."""

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.core.enums import DeviceType
from app.database.config import get_session
from app.device_statistics import events
from app.device_statistics.api.v1.models import (
    DeviceRegistrations,
    SuccessResponse,
    UserLoginEvent,
)

api_router = APIRouter()


@api_router.post("/Log/auth")
def create_user_login_event(
    user_login_event: UserLoginEvent, background_tasks: BackgroundTasks
) -> SuccessResponse:
    """User login event.

    :param user_login_event:
    :param background_tasks:
    :return:
    """
    background_tasks.add_task(
        events.user_login_command, user_login_event.userKey, user_login_event.deviceType
    )
    return SuccessResponse()


@api_router.get("/Log/auth/statistics")
def get_device_registrations(
    deviceType: DeviceType,
    database_session: Session = Depends(get_session),
) -> DeviceRegistrations:
    """Get device registrations.

    :param deviceType:
    :param database_session:
    :return:
    """
    count = events.device_registrations_query(deviceType, database_session)
    response = DeviceRegistrations(deviceType=deviceType, count=count)
    return response
