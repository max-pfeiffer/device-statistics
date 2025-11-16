"""Database configuration."""

from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, Engine
from sqlmodel import Session, create_engine


class DatabaseSettings(BaseSettings):
    """Database settings."""

    user: str
    password: str
    name: str
    host: str
    port: str = "5432"
    alembic_migration_rollback: bool = False
    alembic_migration_revision: str = "INVALID"

    @computed_field
    def database_url(self) -> str:
        """URI for Postgresql database connection.

        :return:
        """
        url_object = URL.create(
            "postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.name,
        )
        return url_object.render_as_string(hide_password=False)

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_", env_file="config/db-alembic.env"
    )


database_settings = DatabaseSettings()

database_engine: Engine = create_engine(database_settings.database_url)


def get_session() -> Generator[Session, Any, None]:
    """Create and yield a database session.

    :return:
    """
    with Session(database_engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
