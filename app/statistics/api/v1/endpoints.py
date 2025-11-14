"""API endpoints."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.config import get_session
from app.statistics.api.v1.models import DeviceRegistrationEvent, SuccessResponse

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
    pass
