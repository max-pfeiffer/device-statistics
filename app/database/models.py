"""Database models."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UserDeviceTypeBase(SQLModel):
    """UserDeviceType."""

    user_key: str
    device_type: str


class UserDeviceType(UserDeviceTypeBase, table=True):
    """Base model."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime
