"""NIOSH publications and FACE reports client (public, no auth)."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class NIOSHClient(BaseAsyncClient):
    """Client for NIOSH publications, FACE reports, and REL data."""

    def __init__(
        self,
        base_url: str = "https://www.cdc.gov/niosh/api",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)

    async def search_publications(self, keyword: str) -> list[dict]:
        """Search NIOSH publications by keyword."""
        resp = await self.get(
            "/publications", params={"keyword": keyword}
        )
        return resp.json()

    async def get_face_reports(
        self,
        industry: str | None = None,
        state: str | None = None,
    ) -> list[dict]:
        """Get FACE (Fatality Assessment and Control Evaluation) reports."""
        params: dict = {}
        if industry:
            params["industry"] = industry
        if state:
            params["state"] = state
        resp = await self.get("/face", params=params)
        return resp.json()

    async def get_rel(self, substance: str) -> dict:
        """Get Recommended Exposure Limit for a substance."""
        resp = await self.get(
            "/rel", params={"substance": substance}
        )
        return resp.json()

    async def get_health_topics(self) -> list[dict]:
        """List available health topic areas."""
        resp = await self.get("/topics")
        return resp.json()
