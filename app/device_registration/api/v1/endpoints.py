"""API endpoints."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.config import get_session
from app.device_registration.api.v1.models import (
    DeviceRegistrationEvent,
    SuccessResponse,
)
from app.device_registration.events import create_device_registration_event

api_router = APIRouter()


@api_router.post("/Device/register")
def register_device_event(
    device_registration_event: DeviceRegistrationEvent,
    database_session: Session = Depends(get_session),
) -> SuccessResponse:
    """Device registration event.

    :param device_registration_event:
    :param database_session:
    :return:
    """
    create_device_registration_event(
        device_registration_event.userKey,
        device_registration_event.deviceType,
        database_session,
    )
    return SuccessResponse()
