"""Uptime Institute Tier certification API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class UptimeInstituteClient(BaseAsyncClient):
    """Client for the Uptime Institute Tier certification API."""

    def __init__(
        self,
        base_url: str = "https://api.uptimeinstitute.com/v1",
        api_key: str | None = None,
        **kwargs,
    ):
        auth_headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
        super().__init__(
            base_url=base_url,
            auth_headers=auth_headers,
            **kwargs,
        )

    async def get_tier_requirements(self, tier_level: str) -> dict:
        """Get requirements for a specific Tier level."""
        resp = await self.get(f"/tiers/{tier_level}/requirements")
        return resp.json()

    async def check_tier_compliance(self, project_id: str, tier_level: str) -> dict:
        """Check project compliance against a Tier level."""
        resp = await self.get(
            f"/projects/{project_id}/compliance",
            params={"tier": tier_level},
        )
        return resp.json()

    async def get_design_documents(self, project_id: str) -> dict:
        """Get design documents for a project."""
        resp = await self.get(f"/projects/{project_id}/design-documents")
        return resp.json()

    async def get_certification_status(self, project_id: str) -> dict:
        """Get certification status for a project."""
        resp = await self.get(f"/projects/{project_id}/certification")
        return resp.json()
