"""Device registration application."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from furl import furl

from app.core.models import ProbeResponse
from app.device_statistics.api.v1.endpoints import api_router
from app.device_statistics.api.v1.models import BadRequestResponse
from app.device_statistics.config import statistics_application_settings

app = FastAPI(
    title=statistics_application_settings.title,
    description=statistics_application_settings.description,
    version=statistics_application_settings.version,
    root_path="/device-statistics",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Override validation exception handler.

    :param request:
    :param exc:
    :return:
    """
    content = BadRequestResponse().model_dump()
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@app.get("/", include_in_schema=False)
def redirect_to_autodocs(request: Request) -> RedirectResponse:
    """Home Page of the application.

    :param Request request:
    :return: RedirectResponse
    """
    furl_item: furl = furl(request.base_url)
    furl_item.path /= app.docs_url.lstrip("/")
    return RedirectResponse(
        furl_item.url, status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


@app.get("/ready", include_in_schema=False)
def readiness_probe() -> ProbeResponse:
    """Readiness probe."""
    return ProbeResponse(status="ready")


@app.get("/healthy", include_in_schema=False)
def health_probe() -> ProbeResponse:
    """Health probe."""
    return ProbeResponse(status="healthy")


app.include_router(api_router, prefix=statistics_application_settings.api_prefix)
