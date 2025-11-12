"""Database configuration."""

from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from app.config import database_settings

database_engine: Engine = create_engine(database_settings.database_url)


def get_session() -> Generator[Session, Any, None]:
    """Create and yield a database session.

    :return:
    """
    with Session(database_engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
