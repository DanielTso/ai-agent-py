"""Schedule query tool for P6/MS Project integration."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class ScheduleQueryTool(Tool):
    """Query and update project schedule activities."""

    name = "schedule_query"
    description = (
        "Query and update project schedule activities"
        " from P6 or MS Project."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_critical_path",
                        "get_activity",
                        "update_activity",
                        "get_float_report",
                    ],
                    "description": "The schedule action to perform.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "activity_id": {
                    "type": "string",
                    "description": "Activity ID (for get/update).",
                },
                "data": {
                    "type": "object",
                    "description": "Data payload for updates.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        activity_id = kwargs.get("activity_id")

        try:
            if action == "get_critical_path":
                return self._get_critical_path(project_id)
            elif action == "get_activity":
                return self._get_activity(project_id, activity_id)
            elif action == "update_activity":
                data = kwargs.get("data", {})
                return self._update_activity(
                    project_id, activity_id, data
                )
            elif action == "get_float_report":
                return self._get_float_report(project_id)
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _get_critical_path(self, project_id: str) -> str:
        today = date.today()
        activities = [
            {
                "id": "ACT-001",
                "external_id": "P6-A1010",
                "name": "Foundation Pour - Zone A",
                "start_date": today.isoformat(),
                "end_date": (today + timedelta(days=14)).isoformat(),
                "total_float": 0.0,
                "is_critical": True,
                "tier_critical": True,
                "predecessors": [],
                "successors": ["ACT-002"],
            },
            {
                "id": "ACT-002",
                "external_id": "P6-A1020",
                "name": "Steel Erection - Zone A",
                "start_date": (
                    today + timedelta(days=15)
                ).isoformat(),
                "end_date": (
                    today + timedelta(days=45)
                ).isoformat(),
                "total_float": 0.0,
                "is_critical": True,
                "tier_critical": True,
                "predecessors": ["ACT-001"],
                "successors": ["ACT-003"],
            },
            {
                "id": "ACT-003",
                "external_id": "P6-A1030",
                "name": "MEP Rough-In - Zone A",
                "start_date": (
                    today + timedelta(days=46)
                ).isoformat(),
                "end_date": (
                    today + timedelta(days=76)
                ).isoformat(),
                "total_float": 0.0,
                "is_critical": True,
                "tier_critical": False,
                "predecessors": ["ACT-002"],
                "successors": ["ACT-004"],
            },
            {
                "id": "ACT-004",
                "external_id": "P6-A1040",
                "name": "Redundant Cooling Loop Install",
                "start_date": (
                    today + timedelta(days=77)
                ).isoformat(),
                "end_date": (
                    today + timedelta(days=107)
                ).isoformat(),
                "total_float": 0.0,
                "is_critical": True,
                "tier_critical": True,
                "predecessors": ["ACT-003"],
                "successors": [],
            },
        ]
        result = {
            "project_id": project_id,
            "critical_path": {
                "activities": activities,
                "total_duration_days": 107,
                "float_summary": {
                    "ACT-001": 0.0,
                    "ACT-002": 0.0,
                    "ACT-003": 0.0,
                    "ACT-004": 0.0,
                },
            },
        }
        return json.dumps(result, indent=2)

    def _get_activity(
        self, project_id: str, activity_id: str | None
    ) -> str:
        if not activity_id:
            return "Error: activity_id is required for get_activity"
        today = date.today()
        activity = {
            "id": activity_id,
            "external_id": f"P6-{activity_id}",
            "name": f"Activity {activity_id}",
            "start_date": today.isoformat(),
            "end_date": (today + timedelta(days=14)).isoformat(),
            "total_float": 3.0,
            "is_critical": False,
            "tier_critical": False,
            "predecessors": [],
            "successors": [],
        }
        return json.dumps(
            {"project_id": project_id, "activity": activity},
            indent=2,
        )

    def _update_activity(
        self,
        project_id: str,
        activity_id: str | None,
        data: dict,
    ) -> str:
        if not activity_id:
            return "Error: activity_id is required for update_activity"
        return json.dumps(
            {
                "project_id": project_id,
                "activity_id": activity_id,
                "status": "updated",
                "updated_fields": list(data.keys()),
            },
            indent=2,
        )

    def _get_float_report(self, project_id: str) -> str:
        report = [
            {
                "activity_id": "ACT-001",
                "activity_name": "Foundation Pour - Zone A",
                "total_float": 0.0,
                "free_float": 0.0,
                "status": "critical",
            },
            {
                "activity_id": "ACT-005",
                "activity_name": "Landscaping - Phase 1",
                "total_float": 15.0,
                "free_float": 10.0,
                "status": "healthy",
            },
            {
                "activity_id": "ACT-006",
                "activity_name": "Elevator Install",
                "total_float": 3.0,
                "free_float": 1.0,
                "status": "warning",
            },
        ]
        return json.dumps(
            {"project_id": project_id, "float_report": report},
            indent=2,
        )
