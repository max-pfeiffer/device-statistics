"""FastAPI application."""

from fastapi import FastAPI

from app.config import application_settings

app = FastAPI(
    title=application_settings.title,
    description=application_settings.description,
    version=application_settings.version,
    root_path="/",
)
