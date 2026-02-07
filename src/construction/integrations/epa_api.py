"""EPA ECHO and enforcement API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class EPAClient(BaseAsyncClient):
    """Client for EPA ECHO facility and compliance APIs."""

    def __init__(
        self,
        base_url: str = "https://api.epa.gov/echo/v1",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)

    async def search_facilities(
        self,
        name: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
    ) -> list[dict]:
        """Search EPA-regulated facilities by name, state, or zip."""
        params: dict = {}
        if name:
            params["facility_name"] = name
        if state:
            params["state_code"] = state
        if zip_code:
            params["zip_code"] = zip_code
        resp = await self.get("/facilities", params=params)
        return resp.json()

    async def get_compliance_history(
        self, facility_id: str
    ) -> dict:
        """Get compliance and enforcement history for a facility."""
        resp = await self.get(
            f"/facilities/{facility_id}/compliance"
        )
        return resp.json()

    async def get_violations(
        self, facility_id: str
    ) -> list[dict]:
        """Get violation records for a facility."""
        resp = await self.get(
            f"/facilities/{facility_id}/violations"
        )
        return resp.json()

    async def get_npdes_permits(
        self, facility_id: str
    ) -> list[dict]:
        """Get NPDES (Clean Water Act) permits for a facility."""
        resp = await self.get(
            f"/facilities/{facility_id}/npdes"
        )
        return resp.json()

    async def get_air_quality(
        self, zip_code: str, parameter: str | None = None
    ) -> dict:
        """Get air quality data for a zip code."""
        params: dict = {"zip_code": zip_code}
        if parameter:
            params["parameter"] = parameter
        resp = await self.get("/air-quality", params=params)
        return resp.json()
