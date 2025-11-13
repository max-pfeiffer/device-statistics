"""Device registration application."""

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from furl import furl

from device_registration.api.v1.endpoints import api_router
from device_registration.config import application_settings

app = FastAPI(
    title=application_settings.title,
    description=application_settings.description,
    version=application_settings.version,
    root_path="/device_registration",
)


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
