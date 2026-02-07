"""ICC building codes API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class ICCClient(BaseAsyncClient):
    """Client for the ICC (International Code Council) codes API."""

    def __init__(
        self,
        base_url: str = "https://api.iccsafe.org/codes/v1",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)

    async def search_codes(
        self,
        code_type: str,
        keyword: str,
    ) -> list[dict]:
        """Search ICC codes by type and keyword.

        code_type examples: IBC, IFC, IMC, IPC, IECC.
        """
        resp = await self.get(
            "/search",
            params={"code_type": code_type, "keyword": keyword},
        )
        return resp.json()

    async def get_code_section(
        self,
        code: str,
        chapter: str,
        section: str,
    ) -> dict:
        """Get a specific code section by code, chapter, and section."""
        resp = await self.get(
            f"/codes/{code}/chapters/{chapter}/sections/{section}",
        )
        return resp.json()

    async def get_occupancy_requirements(
        self, occupancy_type: str
    ) -> list[dict]:
        """Get requirements for a specific occupancy type."""
        resp = await self.get(
            "/occupancy",
            params={"type": occupancy_type},
        )
        return resp.json()

    async def get_structural_requirements(
        self, building_type: str
    ) -> list[dict]:
        """Get structural requirements for a building type."""
        resp = await self.get(
            "/structural",
            params={"building_type": building_type},
        )
        return resp.json()
