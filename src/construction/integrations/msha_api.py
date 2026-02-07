"""MSHA Data Retrieval System client (public, no auth required)."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class MSHAClient(BaseAsyncClient):
    """Client for the MSHA data retrieval APIs."""

    def __init__(
        self,
        base_url: str = "https://api.dol.gov/v2/msha",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)

    async def get_mine_data(self, mine_id: str) -> dict:
        """Get mine details by MSHA mine ID."""
        resp = await self.get(f"/mines/{mine_id}")
        return resp.json()

    async def search_violations(
        self,
        mine_id: str | None = None,
        keyword: str | None = None,
    ) -> list[dict]:
        """Search MSHA violations with optional filters."""
        params: dict = {}
        if mine_id:
            params["mine_id"] = mine_id
        if keyword:
            params["keyword"] = keyword
        resp = await self.get("/violations", params=params)
        return resp.json()

    async def get_inspections(self, mine_id: str) -> list[dict]:
        """Get inspections for a mine."""
        resp = await self.get(
            "/inspections", params={"mine_id": mine_id}
        )
        return resp.json()

    async def check_contractor(self, contractor_id: str) -> dict:
        """Check contractor compliance status."""
        resp = await self.get(f"/contractors/{contractor_id}")
        return resp.json()
