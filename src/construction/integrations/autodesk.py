"""Autodesk ACC / BIM 360 integration client with OAuth 2.0."""

import logging
from datetime import UTC, datetime, timedelta

import httpx

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class AutodeskClient(BaseAsyncClient):
    """Client for Autodesk Construction Cloud / BIM 360 APIs."""

    TOKEN_URL = "https://developer.api.autodesk.com/authentication/v2/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = "https://developer.api.autodesk.com",
        scopes: str = "data:read data:write",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self._access_token: str | None = None
        self._token_expires_at: datetime | None = None

    async def authenticate_2legged(self) -> dict:
        """Obtain a 2-legged OAuth token (client credentials)."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.scopes,
                },
            )
            resp.raise_for_status()
            token_data = resp.json()
        self._apply_token(token_data)
        return token_data

    async def authenticate_3legged(self, authorization_code: str) -> dict:
        """Exchange a 3-legged authorization code for tokens."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": authorization_code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            resp.raise_for_status()
            token_data = resp.json()
        self._apply_token(token_data)
        return token_data

    def _apply_token(self, token_data: dict) -> None:
        self._access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        self._token_expires_at = datetime.now(UTC) + timedelta(
            seconds=expires_in
        )

    async def _ensure_token(self) -> None:
        if self._token_expires_at is None:
            return
        if datetime.now(UTC) >= self._token_expires_at - timedelta(minutes=5):
            await self.authenticate_2legged()

    async def _request(self, method, path, **kwargs) -> httpx.Response:
        await self._ensure_token()
        if self._access_token:
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self._access_token}"
            kwargs["headers"] = headers
        return await super()._request(method, path, **kwargs)

    async def get_hubs(self) -> list[dict]:
        """List all accessible hubs."""
        resp = await self.get("/project/v1/hubs")
        return resp.json().get("data", [])

    async def get_projects(self, hub_id: str) -> list[dict]:
        """List projects within a hub."""
        resp = await self.get(f"/project/v1/hubs/{hub_id}/projects")
        return resp.json().get("data", [])

    async def get_documents(self, project_id: str) -> list[dict]:
        """List top-level documents/folders in a project."""
        resp = await self.get(
            f"/data/v1/projects/{project_id}/folders/root/contents"
        )
        return resp.json().get("data", [])

    async def get_issues(self, project_id: str) -> list[dict]:
        """List issues for a project."""
        resp = await self.get(
            f"/construction/issues/v1/projects/{project_id}/issues"
        )
        return resp.json().get("results", [])

    async def get_model_derivative(self, urn: str) -> dict:
        """Get model derivative manifest for a given URN."""
        resp = await self.get(
            f"/modelderivative/v2/designdata/{urn}/manifest"
        )
        return resp.json()

    async def create_issue(self, project_id: str, data: dict) -> dict:
        """Create an issue in a project."""
        resp = await self.post(
            f"/construction/issues/v1/projects/{project_id}/issues",
            json=data,
        )
        return resp.json()
