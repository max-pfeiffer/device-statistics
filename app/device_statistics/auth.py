"""Authentication."""

import logging

from authlib.jose import JsonWebToken
from authlib.jose.errors import JoseError
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from app.device_statistics.config import statistics_application_settings

logger = logging.getLogger(__name__)


class Scopes(BaseModel):
    """Scopes."""

    scopes: list[str]
    path: str


class JwtBearerAuth(HTTPBearer):
    """Handling authentication for JWT Bearer Authorization."""

    async def __call__(self, request: Request) -> Scopes | None:
        """Handle JWT Bearer Authorization.

        :param request:
        :return:
        """
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                )
            else:
                return None

        # Decode and verify the token contained in credentials
        public_key = statistics_application_settings.idp_public_key
        iss_value = statistics_application_settings.idp_iss
        claim_opts = {}
        claim_opts["iss"] = {"essential": True, "value": iss_value}
        try:
            claims = JsonWebToken("RS256").decode(
                s=credentials, key=public_key, claims_options=claim_opts
            )
            claims.validate()

        except JoseError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        # Getting the scopes Keycloak style
        scopes = claims.get("scope", [])

        return Scopes(scopes=scopes, path=request.url.path)
