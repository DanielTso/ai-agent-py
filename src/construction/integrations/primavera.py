"""Primavera P6 REST API client with API key authentication."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class PrimaveraClient(BaseAsyncClient):
    """Client for Oracle Primavera P6 REST API."""

    def __init__(
        self,
        api_url: str,
        api_key: str,
        **kwargs,
    ):
        super().__init__(
            base_url=api_url,
            auth_headers={"Authorization": f"Bearer {api_key}"},
            **kwargs,
        )

    async def get_activities(self, project_id: str) -> list[dict]:
        """List all activities for a project."""
        resp = await self.get(
            "/activity", params={"ProjectObjectId": project_id}
        )
        return resp.json()

    async def get_relationships(self, project_id: str) -> list[dict]:
        """List activity relationships for a project."""
        resp = await self.get(
            "/relationship", params={"ProjectObjectId": project_id}
        )
        return resp.json()

    async def get_resources(self, project_id: str) -> list[dict]:
        """List resources assigned to a project."""
        resp = await self.get(
            "/resourceassignment",
            params={"ProjectObjectId": project_id},
        )
        return resp.json()

    async def update_activity(
        self, activity_id: str, data: dict
    ) -> dict:
        """Update an activity by its object ID."""
        resp = await self.put(f"/activity/{activity_id}", json=data)
        return resp.json()

    async def get_critical_path(self, project_id: str) -> list[dict]:
        """Retrieve critical-path activities for a project."""
        resp = await self.get(
            "/activity",
            params={
                "ProjectObjectId": project_id,
                "Filter": "IsCritical eq true",
            },
        )
        return resp.json()
