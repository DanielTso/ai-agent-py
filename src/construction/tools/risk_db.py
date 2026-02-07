"""Risk database CRUD tool for the risk register."""

import json
from datetime import UTC, datetime

from ai_agent.tools import Tool


class RiskDatabase(Tool):
    """Query, create, or update risk events in the risk register."""

    name = "risk_database"
    description = (
        "Query, create, or update risk events in the"
        " project risk register. Supports query, create,"
        " and update actions."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["query", "create", "update"],
                    "description": "The action to perform",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project ID",
                },
                "risk_id": {
                    "type": "string",
                    "description": "Risk ID (for update)",
                },
                "filters": {
                    "type": "object",
                    "description": (
                        "Filters for query (e.g. category, status)"
                    ),
                },
                "data": {
                    "type": "object",
                    "description": (
                        "Risk data for create/update"
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
                return self._query(project_id, kwargs.get("filters"))
            elif action == "create":
                return self._create(project_id, kwargs.get("data"))
            elif action == "update":
                return self._update(
                    project_id,
                    kwargs.get("risk_id"),
                    kwargs.get("data"),
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error in risk database: {exc}"

    def _query(
        self, project_id: str, filters: dict | None
    ) -> str:
        category = (filters or {}).get("category")
        status = (filters or {}).get("status", "active")

        risks = [
            {
                "id": "RISK-001",
                "project_id": project_id,
                "category": "weather",
                "description": (
                    "Severe thunderstorms forecast for week 3"
                    " may halt exterior concrete pours"
                ),
                "probability": 0.35,
                "impact_dollars": 250000,
                "impact_days": 5,
                "safety_critical": False,
                "confidence": 0.78,
                "status": "active",
            },
            {
                "id": "RISK-002",
                "project_id": project_id,
                "category": "supply",
                "description": (
                    "Structural steel delivery delayed —"
                    " port congestion at Houston"
                ),
                "probability": 0.60,
                "impact_dollars": 500000,
                "impact_days": 14,
                "safety_critical": False,
                "confidence": 0.85,
                "status": "active",
            },
            {
                "id": "RISK-003",
                "project_id": project_id,
                "category": "safety",
                "description": (
                    "Crane proximity to power lines during"
                    " steel erection phase"
                ),
                "probability": 0.15,
                "impact_dollars": 1000000,
                "impact_days": 30,
                "safety_critical": True,
                "confidence": 0.92,
                "status": "active",
            },
        ]

        if category:
            risks = [r for r in risks if r["category"] == category]
        if status:
            risks = [r for r in risks if r["status"] == status]

        return json.dumps(
            {"risks": risks, "total": len(risks)}, indent=2
        )

    def _create(self, project_id: str, data: dict | None) -> str:
        if not data:
            return "Error: data is required for create action"
        now = datetime.now(UTC).isoformat()
        risk = {
            "id": f"RISK-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            "project_id": project_id,
            "created_at": now,
            **data,
        }
        return json.dumps(
            {"created": risk, "status": "success"}, indent=2
        )

    def _update(
        self,
        project_id: str,
        risk_id: str | None,
        data: dict | None,
    ) -> str:
        if not risk_id:
            return "Error: risk_id is required for update action"
        if not data:
            return "Error: data is required for update action"
        now = datetime.now(UTC).isoformat()
        updated = {
            "id": risk_id,
            "project_id": project_id,
            "updated_at": now,
            **data,
        }
        return json.dumps(
            {"updated": updated, "status": "success"}, indent=2
        )
