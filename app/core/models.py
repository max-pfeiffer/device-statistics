"""Core models."""

from pydantic import BaseModel


class ProbeResponse(BaseModel):
    """Probe response."""

    status: str
