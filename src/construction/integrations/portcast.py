"""Portcast container tracking API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class PortcastClient(BaseAsyncClient):
    """Client for the Portcast container tracking API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.portcast.io/api/v1",
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            auth_headers={"x-api-key": api_key},
            **kwargs,
        )

    async def track_container(self, container_id: str) -> dict:
        """Get tracking data for a container."""
        resp = await self.get(f"/tracking/{container_id}")
        return resp.json()

    async def get_port_congestion(self, port_code: str) -> dict:
        """Get congestion data for a port."""
        resp = await self.get(f"/ports/{port_code}/congestion")
        return resp.json()

    async def get_vessel_position(self, vessel_imo: str) -> dict:
        """Get current position of a vessel by IMO number."""
        resp = await self.get(f"/vessels/{vessel_imo}/position")
        return resp.json()
