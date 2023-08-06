"""
Authentication Manager
Authenticate with Microsoft Online.
"""
from abc import ABC, abstractmethod
import logging
from typing import Any, List, Optional

from aiohttp import hdrs
import aiohttp
from aiohttp.client import ClientSession, ClientResponse
from yarl import URL

from .models import OAuth2TokenResponse

log = logging.getLogger("authentication")

DEFAULT_SCOPES = ["https://graph.microsoft.com/.default", "offline_access"]
AUTHORITY = "https://login.microsoftonline.com/common"

class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, client_session: ClientSession):
        self.session: ClientSession = client_session

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.session.request(
            method, url, **kwargs, headers=headers,
        )

    async def get(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_GET, url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_OPTIONS, url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_HEAD, url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_POST, url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_PUT, url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_PATCH, url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_DELETE, url, **kwargs)


class AuthManager(AbstractAuth):
    def __init__(
        self,
        client_session: ClientSession,

        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None,
    ):
        self.session: ClientSession = client_session
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_uri: str = redirect_uri
        self._scopes: List[str] = scopes or DEFAULT_SCOPES

        self.oauth: OAuth2TokenResponse = None


    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if not self.oauth:
            raise NotAuthenticated()

        if not self.oauth.is_valid():
            await self.refresh_token()

        return self.oauth.access_token


    def generate_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate Microsoft Authorization URL."""
        query_string = {
            "client_id": self._client_id,
            "response_type": "code",
            "response_mode": "query",
            "approval_prompt": "auto",
            "scope": " ".join(self._scopes),
            "redirect_uri": self._redirect_uri,
        }

        if state:
            query_string["state"] = state

        return str(
            URL(AUTHORITY + "/oauth2/v2.0/authorize").with_query(query_string)
        )


    async def request_token(self, authorization_code: str) -> None:
        """Request OAuth2 token."""
        self.oauth = await self._oauth2_token_request(
            {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "scope": " ".join(self._scopes),
                "redirect_uri": self._redirect_uri,
            }
        )

    async def refresh_token(self) -> None:
        """Refresh OAuth2 token."""
        self.oauth = await self._oauth2_token_request(
            {
                "grant_type": "refresh_token",
                "scope": " ".join(self._scopes),
                "refresh_token": self.oauth.refresh_token,
            }
        )

    async def _oauth2_token_request(self, data: dict) -> OAuth2TokenResponse:
        """Execute token requests."""
        data["client_id"] = self._client_id
        if self._client_secret:
            data["client_secret"] = self._client_secret 
        resp = await self.session.post(
            AUTHORITY + "/oauth2/v2.0/token", data=data
        )
        resp.raise_for_status()
        return OAuth2TokenResponse.parse_raw(await resp.text())


class NotAuthenticated(Exception):
    """User not authenticated."""
