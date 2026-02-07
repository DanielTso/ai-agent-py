"""Workforce query tool for crew status, productivity, and certs."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class WorkforceQuery(Tool):
    """Query workforce data including crew status and productivity."""

    name = "workforce_query"
    description = (
        "Query workforce data including crew status,"
        " productivity, and certifications."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "crew_status",
                        "productivity",
                        "certifications",
                        "labor_forecast",
                    ],
                    "description": "The workforce query to perform",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project ID",
                },
                "trade": {
                    "type": "string",
                    "description": (
                        "Filter by trade (e.g. electrical,"
                        " mechanical)"
                    ),
                },
                "worker_id": {
                    "type": "string",
                    "description": "Filter by worker ID",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "crew_status":
                return self._crew_status(
                    project_id, kwargs.get("trade")
                )
            elif action == "productivity":
                return self._productivity(
                    project_id, kwargs.get("trade")
                )
            elif action == "certifications":
                return self._certifications(
                    project_id, kwargs.get("worker_id")
                )
            elif action == "labor_forecast":
                return self._labor_forecast(
                    project_id, kwargs.get("trade")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error in workforce query: {exc}"

    def _crew_status(
        self, project_id: str, trade: str | None
    ) -> str:
        crews = [
            {
                "trade": "electrical",
                "headcount": 24,
                "planned_production": 150.0,
                "actual_production": 138.0,
                "productivity_pct": 92.0,
                "location": "Building A — Level 3",
                "overtime_hours": 12.5,
            },
            {
                "trade": "mechanical",
                "headcount": 18,
                "planned_production": 120.0,
                "actual_production": 125.0,
                "productivity_pct": 104.2,
                "location": "Building B — Penthouse",
                "overtime_hours": 4.0,
            },
            {
                "trade": "plumbing",
                "headcount": 12,
                "planned_production": 80.0,
                "actual_production": 68.0,
                "productivity_pct": 85.0,
                "location": "Building A — Level 1",
                "overtime_hours": 18.0,
            },
            {
                "trade": "fire_protection",
                "headcount": 8,
                "planned_production": 60.0,
                "actual_production": 55.0,
                "productivity_pct": 91.7,
                "location": "Building A — Level 2",
                "overtime_hours": 6.0,
            },
        ]
        if trade:
            crews = [c for c in crews if c["trade"] == trade]
        return json.dumps(
            {"crews": crews, "note": "Mock data"}, indent=2
        )

    def _productivity(
        self, project_id: str, trade: str | None
    ) -> str:
        metrics = [
            {
                "trade": "electrical",
                "period": "2025-W26",
                "planned_units": 150.0,
                "actual_units": 138.0,
                "productivity_index": 0.92,
                "trend": "declining",
            },
            {
                "trade": "mechanical",
                "period": "2025-W26",
                "planned_units": 120.0,
                "actual_units": 125.0,
                "productivity_index": 1.04,
                "trend": "improving",
            },
            {
                "trade": "plumbing",
                "period": "2025-W26",
                "planned_units": 80.0,
                "actual_units": 68.0,
                "productivity_index": 0.85,
                "trend": "declining",
            },
            {
                "trade": "fire_protection",
                "period": "2025-W26",
                "planned_units": 60.0,
                "actual_units": 55.0,
                "productivity_index": 0.92,
                "trend": "stable",
            },
        ]
        if trade:
            metrics = [
                m for m in metrics if m["trade"] == trade
            ]
        return json.dumps(
            {"productivity": metrics, "note": "Mock data"},
            indent=2,
        )

    def _certifications(
        self, project_id: str, worker_id: str | None
    ) -> str:
        today = date.today()
        certs = [
            {
                "worker_id": "WRK-101",
                "worker_name": "Mike Johnson",
                "cert_type": "OSHA30",
                "issue_date": "2022-06-15",
                "expiry_date": (
                    today + timedelta(days=15)
                ).isoformat(),
                "status": "expiring_soon",
            },
            {
                "worker_id": "WRK-205",
                "worker_name": "Sarah Chen",
                "cert_type": "BICSI",
                "issue_date": "2023-01-10",
                "expiry_date": (
                    today + timedelta(days=90)
                ).isoformat(),
                "status": "valid",
            },
            {
                "worker_id": "WRK-312",
                "worker_name": "James Williams",
                "cert_type": "NETA",
                "issue_date": "2021-03-20",
                "expiry_date": (
                    today - timedelta(days=10)
                ).isoformat(),
                "status": "expired",
            },
            {
                "worker_id": "WRK-408",
                "worker_name": "Ana Rodriguez",
                "cert_type": "competent_person",
                "issue_date": "2024-01-05",
                "expiry_date": (
                    today + timedelta(days=7)
                ).isoformat(),
                "status": "expiring_soon",
            },
        ]
        if worker_id:
            certs = [
                c for c in certs if c["worker_id"] == worker_id
            ]
        return json.dumps(
            {"certifications": certs, "note": "Mock data"},
            indent=2,
        )

    def _labor_forecast(
        self, project_id: str, trade: str | None
    ) -> str:
        forecasts = [
            {
                "trade": "electrical",
                "week": "2025-W27",
                "required_headcount": 30,
                "available_headcount": 24,
                "gap": 6,
                "critical": True,
            },
            {
                "trade": "mechanical",
                "week": "2025-W27",
                "required_headcount": 18,
                "available_headcount": 18,
                "gap": 0,
                "critical": False,
            },
            {
                "trade": "plumbing",
                "week": "2025-W27",
                "required_headcount": 15,
                "available_headcount": 12,
                "gap": 3,
                "critical": True,
            },
            {
                "trade": "fire_protection",
                "week": "2025-W27",
                "required_headcount": 10,
                "available_headcount": 8,
                "gap": 2,
                "critical": False,
            },
        ]
        if trade:
            forecasts = [
                f for f in forecasts if f["trade"] == trade
            ]
        return json.dumps(
            {"labor_forecast": forecasts, "note": "Mock data"},
            indent=2,
        )
