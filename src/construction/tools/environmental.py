"""Environmental query tool for permits, LEED, carbon, and SWPPP."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class EnvironmentalQuery(Tool):
    """Query environmental compliance and sustainability data."""

    name = "environmental_query"
    description = (
        "Query environmental data including permits,"
        " LEED credits, carbon metrics, and SWPPP checks."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "permits",
                        "leed_credits",
                        "carbon",
                        "swppp_check",
                    ],
                    "description": "The environmental action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "permit_type": {
                    "type": "string",
                    "description": (
                        "Filter by permit type"
                        " (SWPPP/air/noise/water/waste)."
                    ),
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "permits":
                return self._permits(
                    project_id, kwargs.get("permit_type")
                )
            elif action == "leed_credits":
                return self._leed_credits(project_id)
            elif action == "carbon":
                return self._carbon(project_id)
            elif action == "swppp_check":
                return self._swppp_check(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _permits(
        self, project_id: str, permit_type: str | None
    ) -> str:
        today = date.today()
        permits = [
            {
                "id": "PRM-001",
                "permit_type": "SWPPP",
                "status": "active",
                "expiry": (
                    today + timedelta(days=180)
                ).isoformat(),
                "last_inspection": (
                    today - timedelta(days=14)
                ).isoformat(),
                "conditions": [
                    "Weekly site inspections",
                    "Silt fence maintenance",
                    "Inlet protection required",
                ],
            },
            {
                "id": "PRM-002",
                "permit_type": "noise",
                "status": "active",
                "expiry": (
                    today + timedelta(days=90)
                ).isoformat(),
                "last_inspection": None,
                "conditions": [
                    "No work before 7AM or after 6PM",
                    "85 dBA limit at property line",
                ],
            },
            {
                "id": "PRM-003",
                "permit_type": "air",
                "status": "expiring",
                "expiry": (
                    today + timedelta(days=15)
                ).isoformat(),
                "last_inspection": (
                    today - timedelta(days=60)
                ).isoformat(),
                "conditions": [
                    "Dust suppression during demolition",
                    "Monitor PM2.5 at boundary",
                ],
            },
            {
                "id": "PRM-004",
                "permit_type": "water",
                "status": "active",
                "expiry": (
                    today + timedelta(days=365)
                ).isoformat(),
                "last_inspection": (
                    today - timedelta(days=30)
                ).isoformat(),
                "conditions": [
                    "Dewatering discharge monitoring",
                    "pH testing of discharge",
                ],
            },
        ]
        if permit_type:
            permits = [
                p for p in permits
                if p["permit_type"] == permit_type
            ]
        return json.dumps(
            {
                "project_id": project_id,
                "permits": permits,
                "note": "Mock data",
            },
            indent=2,
        )

    def _leed_credits(self, project_id: str) -> str:
        credits = [
            {
                "credit_id": "EAc1",
                "category": "energy",
                "points": 8.0,
                "max_points": 10.0,
                "status": "earned",
                "documentation": "Energy model complete",
            },
            {
                "credit_id": "WEc1",
                "category": "water",
                "points": 3.0,
                "max_points": 4.0,
                "status": "pending",
                "documentation": (
                    "Fixture calcs submitted"
                ),
            },
            {
                "credit_id": "MRc2",
                "category": "materials",
                "points": 1.0,
                "max_points": 2.0,
                "status": "at_risk",
                "documentation": None,
            },
            {
                "credit_id": "EQc1",
                "category": "indoor_quality",
                "points": 0.0,
                "max_points": 3.0,
                "status": "not_pursued",
                "documentation": None,
            },
            {
                "credit_id": "INc1",
                "category": "innovation",
                "points": 1.0,
                "max_points": 1.0,
                "status": "earned",
                "documentation": "Green education program",
            },
        ]
        total = sum(c["points"] for c in credits)
        max_total = sum(c["max_points"] for c in credits)
        return json.dumps(
            {
                "project_id": project_id,
                "leed_credits": credits,
                "total_points": total,
                "max_points": max_total,
                "note": "Mock data",
            },
            indent=2,
        )

    def _carbon(self, project_id: str) -> str:
        metrics = [
            {
                "period": "2025-Q1",
                "scope": "scope1",
                "emissions_mt": 120.5,
                "target_mt": 130.0,
                "variance_pct": -7.3,
            },
            {
                "period": "2025-Q1",
                "scope": "scope2",
                "emissions_mt": 85.2,
                "target_mt": 80.0,
                "variance_pct": 6.5,
            },
            {
                "period": "2025-Q1",
                "scope": "scope3",
                "emissions_mt": 340.0,
                "target_mt": 350.0,
                "variance_pct": -2.9,
            },
            {
                "period": "2025-Q2",
                "scope": "scope1",
                "emissions_mt": 115.0,
                "target_mt": 125.0,
                "variance_pct": -8.0,
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "carbon_metrics": metrics,
                "note": "Mock data",
            },
            indent=2,
        )

    def _swppp_check(self, project_id: str) -> str:
        today = date.today()
        checks = [
            {
                "date": (
                    today - timedelta(days=7)
                ).isoformat(),
                "inspector": "John Smith, CPESC",
                "findings": [
                    "Silt fence intact — north perimeter",
                    "Inlet protection in place",
                    "Minor sediment accumulation at SW corner",
                ],
                "corrective_actions": [
                    "Clean sediment at SW corner by Friday",
                ],
                "compliant": True,
            },
            {
                "date": (
                    today - timedelta(days=14)
                ).isoformat(),
                "inspector": "John Smith, CPESC",
                "findings": [
                    "Silt fence damage — east perimeter",
                    "Stockpile not covered",
                ],
                "corrective_actions": [
                    "Repair silt fence immediately",
                    "Cover stockpile with tarp",
                ],
                "compliant": False,
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "swppp_checks": checks,
                "note": "Mock data",
            },
            indent=2,
        )
