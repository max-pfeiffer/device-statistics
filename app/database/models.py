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


class UserDeviceTypeWrite(UserDeviceTypeBase):
    """UserDeviceTypeWrite."""

    pass


class UserDeviceTypeRead(UserDeviceTypeBase):
    """UserDeviceTypeRead."""

    id: UUID


# This model/table is for handling database schema migrations in the deployment process
class MigrationMetaData(SQLModel):
    """MigrationMetaData."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    after_migration_revision: str
    before_migration_revision: str
    rolled_back: str
