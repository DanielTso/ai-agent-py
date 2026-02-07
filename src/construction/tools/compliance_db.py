"""Compliance ticket CRUD tool."""

import json
from datetime import UTC, datetime

from ai_agent.tools import Tool


class ComplianceDatabaseTool(Tool):
    """Query, create, or update compliance checks and deviation tickets."""

    name = "compliance_database"
    description = (
        "Query, create, or update compliance checks"
        " and deviation tickets."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "query",
                        "create",
                        "update",
                        "get_summary",
                    ],
                    "description": (
                        "The compliance database action."
                    ),
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "check_id": {
                    "type": "string",
                    "description": (
                        "Compliance check ID for"
                        " get/update operations."
                    ),
                },
                "filters": {
                    "type": "object",
                    "description": (
                        "Filters for query (severity,"
                        " status, check_type)."
                    ),
                },
                "data": {
                    "type": "object",
                    "description": (
                        "Data payload for create/update."
                    ),
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]

        try:
            if action == "query":
                return self._query(
                    project_id, kwargs.get("filters")
                )
            elif action == "create":
                return self._create(
                    project_id, kwargs.get("data", {})
                )
            elif action == "update":
                return self._update(
                    project_id,
                    kwargs.get("check_id"),
                    kwargs.get("data", {}),
                )
            elif action == "get_summary":
                return self._get_summary(project_id)
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _query(
        self, project_id: str, filters: dict | None
    ) -> str:
        now = datetime.now(UTC).isoformat()
        checks = [
            {
                "id": "CHK-001",
                "project_id": project_id,
                "check_type": "fire_separation",
                "severity": "critical",
                "status": "open",
                "location": "Level 3, Grid B-4",
                "description": (
                    "Fire wall rating 1.5hr vs 2hr required"
                ),
                "created_at": now,
            },
            {
                "id": "CHK-002",
                "project_id": project_id,
                "check_type": "redundancy_path",
                "severity": "critical",
                "status": "open",
                "location": "Mechanical Room 2B",
                "description": (
                    "Missing redundant cooling loop path"
                ),
                "created_at": now,
            },
            {
                "id": "CHK-003",
                "project_id": project_id,
                "check_type": "egress",
                "severity": "major",
                "status": "in_progress",
                "location": "Level 1, Exit B",
                "description": "Egress door width under minimum",
                "created_at": now,
            },
        ]
        if filters:
            severity = filters.get("severity")
            status = filters.get("status")
            check_type = filters.get("check_type")
            if severity:
                checks = [
                    c for c in checks
                    if c["severity"] == severity
                ]
            if status:
                checks = [
                    c for c in checks
                    if c["status"] == status
                ]
            if check_type:
                checks = [
                    c for c in checks
                    if c["check_type"] == check_type
                ]
        return json.dumps(
            {"project_id": project_id, "checks": checks},
            indent=2,
        )

    def _create(self, project_id: str, data: dict) -> str:
        check_id = f"CHK-{datetime.now(UTC).strftime('%H%M%S')}"
        return json.dumps(
            {
                "project_id": project_id,
                "check_id": check_id,
                "status": "created",
                "data": data,
            },
            indent=2,
        )

    def _update(
        self,
        project_id: str,
        check_id: str | None,
        data: dict,
    ) -> str:
        if not check_id:
            return "Error: check_id is required for update"
        return json.dumps(
            {
                "project_id": project_id,
                "check_id": check_id,
                "status": "updated",
                "updated_fields": list(data.keys()),
            },
            indent=2,
        )

    def _get_summary(self, project_id: str) -> str:
        return json.dumps(
            {
                "project_id": project_id,
                "total_checks": 15,
                "total_open": 5,
                "critical_count": 2,
                "major_count": 2,
                "minor_count": 1,
                "by_type": {
                    "fire_separation": 3,
                    "redundancy_path": 4,
                    "egress": 3,
                    "bim_vs_field": 3,
                    "code_compliance": 2,
                },
            },
            indent=2,
        )
