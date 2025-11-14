"""API endpoints."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from app.core.enums import DeviceType
from app.database.config import get_session
from app.device_statistics import events
from app.device_statistics.api.v1.models import (
    DeviceRegistrations,
    SuccessResponse,
    UserLoginEvent,
)
from app.device_statistics.auth import JwtBearerAuth, Scopes

jwt_bearer_auth = JwtBearerAuth()

api_router = APIRouter()


@api_router.post("/Log/auth")
def create_user_login_event(
    user_login_event: UserLoginEvent,
    background_tasks: BackgroundTasks,
    scopes: Annotated[Scopes, Depends(jwt_bearer_auth)],
) -> SuccessResponse:
    """User login event.

    :param user_login_event:
    :param scopes:
    :param background_tasks:
    :return:
    """
    # Resource Authorization
    if "login" not in scopes.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    background_tasks.add_task(
        events.user_login_command, user_login_event.userKey, user_login_event.deviceType
    )
    return SuccessResponse()


@api_router.get("/Log/auth/statistics")
def get_device_registrations(
    deviceType: DeviceType,
    scopes: Annotated[Scopes, Depends(jwt_bearer_auth)],
    database_session: Session = Depends(get_session),
) -> DeviceRegistrations:
    """Get device registrations.

    :param deviceType:
    :param scopes:
    :param database_session:
    :return:
    """
    # Resource Authorization
    if "statistics" not in scopes.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    count = events.device_registrations_query(deviceType, database_session)
    response = DeviceRegistrations(deviceType=deviceType, count=count)
    return response
