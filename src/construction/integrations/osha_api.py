"""OSHA ITA and enforcement API client (public, no auth required)."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class OSHAClient(BaseAsyncClient):
    """Client for the OSHA enforcement and ITA data APIs."""

    def __init__(
        self,
        base_url: str = "https://enforcedata.dol.gov/api",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)

    async def search_inspections(
        self,
        establishment: str | None = None,
        state: str | None = None,
        sic: str | None = None,
    ) -> list[dict]:
        """Search OSHA inspections with optional filters."""
        params: dict = {}
        if establishment:
            params["estab_name"] = establishment
        if state:
            params["site_state"] = state
        if sic:
            params["sic_code"] = sic
        resp = await self.get("/inspection", params=params)
        return resp.json()

    async def get_citations(self, inspection_id: str) -> list[dict]:
        """Get citations for a specific inspection."""
        resp = await self.get(f"/inspection/{inspection_id}/citation")
        return resp.json()

    async def get_300a_data(
        self, establishment: str, year: int
    ) -> list[dict]:
        """Get OSHA 300A summary data for an establishment."""
        resp = await self.get(
            "/ita",
            params={"estab_name": establishment, "year": year},
        )
        return resp.json()

    async def search_violations(self, keyword: str) -> list[dict]:
        """Search violation descriptions by keyword."""
        resp = await self.get(
            "/violation", params={"keyword": keyword}
        )
        return resp.json()
