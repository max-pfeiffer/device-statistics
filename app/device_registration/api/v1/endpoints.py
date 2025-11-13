"""API endpoints."""

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.database.config import get_session
from device_registration.api.v1.models import (
    DeviceRegistrations,
    SuccessResponse,
    UserLoginEvent,
)
from device_registration.events import device_registrations_query, user_login_command

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
        user_login_command, user_login_event.userKey, user_login_event.deviceType
    )
    return SuccessResponse()


@api_router.get("/Log/auth/statistics")
def get_device_registrations(
    deviceType: str,
    database_session: Session = Depends(get_session),
) -> DeviceRegistrations:
    """Get device registrations.

    :param deviceType:
    :param database_session:
    :return:
    """
    response = device_registrations_query(deviceType, database_session)
    return response
