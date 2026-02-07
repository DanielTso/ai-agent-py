"""Vizion container tracking API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class VizionClient(BaseAsyncClient):
    """Client for the Vizion container visibility API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.vizionapi.com/api/v2",
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            auth_headers={"X-API-Key": api_key},
            **kwargs,
        )

    async def get_container(self, container_id: str) -> dict:
        """Get container tracking details."""
        resp = await self.get(f"/containers/{container_id}")
        return resp.json()

    async def get_eta(self, container_id: str) -> dict:
        """Get estimated time of arrival for a container."""
        resp = await self.get(f"/containers/{container_id}/eta")
        return resp.json()

    async def list_containers(self) -> list[dict]:
        """List all tracked containers."""
        resp = await self.get("/containers")
        return resp.json()
