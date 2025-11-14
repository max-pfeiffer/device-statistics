"""Device registration application."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from furl import furl

from app.device_registration.api.v1.endpoints import api_router
from app.device_registration.api.v1.models import ErrorResponse
from app.device_registration.config import application_settings

app = FastAPI(
    title=application_settings.title,
    description=application_settings.description,
    version=application_settings.version,
    root_path="/device_registration",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Override validation exception handler.

    :param request:
    :param exc:
    :return:
    """
    content = ErrorResponse().model_dump()
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


app.include_router(api_router, prefix=application_settings.api_prefix)
