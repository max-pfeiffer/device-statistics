"""API models."""

from pydantic import BaseModel

from app.core.enums import DeviceType


class UserLoginEvent(BaseModel):
    """User login event."""

    userKey: str
    deviceType: DeviceType


class DeviceRegistrations(BaseModel):
    """Device registrations."""

    deviceType: DeviceType
    count: int


class SuccessResponse(BaseModel):
    """Success response."""

    statusCode: int = 200
    message: int = "success"


class ErrorResponse(BaseModel):
    """Error response."""

    statusCode: int = 400
    message: int = "bad_request"
