"""Models."""

from pydantic import BaseModel

from app.core.enums import DeviceType


class DeviceRegistrationEvent(BaseModel):
    """Device registration event."""

    userKey: str
    deviceType: DeviceType


class SuccessResponse(BaseModel):
    """Success response."""

    statusCode: int = 200


class BadRequestResponse(BaseModel):
    """Bad request response."""

    statusCode: int = 400
