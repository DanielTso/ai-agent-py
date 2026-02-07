"""Procore integration client with OAuth 2.0 token management."""

import logging
from datetime import UTC, datetime, timedelta

import httpx

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class ProcoreClient(BaseAsyncClient):
    """Client for the Procore Construction Management API."""

    TOKEN_URL = "https://login.procore.com/oauth/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "",
        base_url: str = "https://api.procore.com/rest/v1.0",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._token_expires_at: datetime | None = None

    async def authenticate(self, authorization_code: str) -> dict:
        """Exchange authorization code for access + refresh tokens."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": authorization_code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                },
            )
            resp.raise_for_status()
            token_data = resp.json()
        self._apply_token(token_data)
        return token_data

    async def _refresh_access_token(self) -> None:
        """Refresh the OAuth 2.0 access token."""
        if not self._refresh_token:
            raise RuntimeError("No refresh token available")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self._refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            resp.raise_for_status()
            token_data = resp.json()
        self._apply_token(token_data)

    def _apply_token(self, token_data: dict) -> None:
        self._access_token = token_data["access_token"]
        self._refresh_token = token_data.get(
            "refresh_token", self._refresh_token
        )
        expires_in = token_data.get("expires_in", 7200)
        self._token_expires_at = datetime.now(UTC) + timedelta(
            seconds=expires_in
        )

    async def _ensure_token(self) -> None:
        """Refresh token if expired or about to expire."""
        if self._token_expires_at is None:
            return
        if datetime.now(UTC) >= self._token_expires_at - timedelta(minutes=5):
            await self._refresh_access_token()

    async def _request(self, method, path, **kwargs) -> httpx.Response:
        await self._ensure_token()
        if self._access_token:
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self._access_token}"
            kwargs["headers"] = headers
        return await super()._request(method, path, **kwargs)

    async def get_projects(self) -> list[dict]:
        """List all projects accessible to the authenticated user."""
        resp = await self.get("/projects")
        return resp.json()

    async def get_documents(self, project_id: int) -> list[dict]:
        """List documents for a project."""
        resp = await self.get(f"/projects/{project_id}/documents")
        return resp.json()

    async def get_rfis(self, project_id: int) -> list[dict]:
        """List RFIs for a project."""
        resp = await self.get(f"/projects/{project_id}/rfis")
        return resp.json()

    async def get_submittals(self, project_id: int) -> list[dict]:
        """List submittals for a project."""
        resp = await self.get(f"/projects/{project_id}/submittals")
        return resp.json()

    async def create_rfi(self, project_id: int, data: dict) -> dict:
        """Create a new RFI in a project."""
        resp = await self.post(
            f"/projects/{project_id}/rfis", json=data
        )
        return resp.json()

    async def update_submittal(
        self, project_id: int, submittal_id: int, data: dict
    ) -> dict:
        """Update a submittal in a project."""
        resp = await self.put(
            f"/projects/{project_id}/submittals/{submittal_id}",
            json=data,
        )
        return resp.json()
