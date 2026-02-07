"""Terminal49 shipment tracking API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class Terminal49Client(BaseAsyncClient):
    """Client for the Terminal49 shipment tracking API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.terminal49.com/v2",
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            auth_headers={"Authorization": f"Token {api_key}"},
            **kwargs,
        )

    async def get_shipments(self) -> list[dict]:
        """List all shipments."""
        resp = await self.get("/shipments")
        return resp.json().get("data", [])

    async def get_shipment(self, shipment_id: str) -> dict:
        """Get details for a specific shipment."""
        resp = await self.get(f"/shipments/{shipment_id}")
        return resp.json().get("data", {})

    async def get_milestones(self, shipment_id: str) -> list[dict]:
        """Get tracking milestones for a shipment."""
        resp = await self.get(
            f"/shipments/{shipment_id}/transport_events"
        )
        return resp.json().get("data", [])

    async def create_tracking(self, tracking_data: dict) -> dict:
        """Create a new tracking request."""
        resp = await self.post("/tracking_requests", json=tracking_data)
        return resp.json().get("data", {})
