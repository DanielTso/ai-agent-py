"""Microsoft Project REST API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class MSProjectClient(BaseAsyncClient):
    """Client for Microsoft Project Online / Server REST API."""

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

    async def get_tasks(self, project_id: str) -> list[dict]:
        """List all tasks for a project."""
        resp = await self.get(f"/projects/{project_id}/tasks")
        return resp.json()

    async def get_assignments(self, project_id: str) -> list[dict]:
        """List resource assignments for a project."""
        resp = await self.get(f"/projects/{project_id}/assignments")
        return resp.json()

    async def get_calendars(self, project_id: str) -> list[dict]:
        """List calendars for a project."""
        resp = await self.get(f"/projects/{project_id}/calendars")
        return resp.json()

    async def update_task(
        self, project_id: str, task_id: str, data: dict
    ) -> dict:
        """Update a task within a project."""
        resp = await self.put(
            f"/projects/{project_id}/tasks/{task_id}", json=data
        )
        return resp.json()
