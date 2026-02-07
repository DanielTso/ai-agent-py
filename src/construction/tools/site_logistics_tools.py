"""Site logistics query tool for crane, staging, and headcount."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class SiteLogisticsQuery(Tool):
    """Query site logistics data."""

    name = "site_logistics_query"
    description = (
        "Query site logistics including crane schedules,"
        " staging plans, headcount, and site permits."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "crane_schedule",
                        "staging",
                        "headcount",
                        "permits",
                    ],
                    "description": "The logistics action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "date": {
                    "type": "string",
                    "description": "Date filter (YYYY-MM-DD).",
                },
                "trade": {
                    "type": "string",
                    "description": "Trade filter.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "crane_schedule":
                return self._crane_schedule(project_id)
            elif action == "staging":
                return self._staging(project_id)
            elif action == "headcount":
                return self._headcount(
                    project_id, kwargs.get("trade")
                )
            elif action == "permits":
                return self._permits(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _crane_schedule(self, project_id: str) -> str:
        today = date.today()
        entries = [
            {
                "crane_id": "TC-01",
                "date": today.isoformat(),
                "time_slot": "07:00-09:00",
                "trade": "steel",
                "activity": "Steel beam lift — Level 5",
                "weight_tons": 12.5,
                "duration_hours": 2.0,
                "status": "scheduled",
            },
            {
                "crane_id": "TC-01",
                "date": today.isoformat(),
                "time_slot": "09:30-11:30",
                "trade": "mechanical",
                "activity": "AHU placement — Roof",
                "weight_tons": 8.0,
                "duration_hours": 2.0,
                "status": "scheduled",
            },
            {
                "crane_id": "TC-01",
                "date": today.isoformat(),
                "time_slot": "13:00-15:00",
                "trade": "concrete",
                "activity": "Concrete bucket — Level 4",
                "weight_tons": 4.5,
                "duration_hours": 2.0,
                "status": "scheduled",
            },
            {
                "crane_id": "TC-02",
                "date": today.isoformat(),
                "time_slot": "07:00-10:00",
                "trade": "steel",
                "activity": "Curtain wall panel lift",
                "weight_tons": 3.2,
                "duration_hours": 3.0,
                "status": "in_progress",
            },
            {
                "crane_id": "TC-01",
                "date": (
                    today + timedelta(days=1)
                ).isoformat(),
                "time_slot": "07:00-09:00",
                "trade": "steel",
                "activity": (
                    "Steel column lift — Level 6"
                ),
                "weight_tons": 15.0,
                "duration_hours": 2.0,
                "status": "scheduled",
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "crane_schedule": entries,
                "note": "Mock data",
            },
            indent=2,
        )

    def _staging(self, project_id: str) -> str:
        zones = [
            {
                "zone_id": "STG-A",
                "zone_name": "North Laydown",
                "capacity_sqft": 5000.0,
                "current_usage_sqft": 4200.0,
                "utilization_pct": 84.0,
                "materials": [
                    "Rebar bundles",
                    "Formwork panels",
                    "Concrete accessories",
                ],
                "trade": "concrete",
            },
            {
                "zone_id": "STG-B",
                "zone_name": "South Laydown",
                "capacity_sqft": 3000.0,
                "current_usage_sqft": 1500.0,
                "utilization_pct": 50.0,
                "materials": [
                    "Ductwork sections",
                    "Pipe spools",
                ],
                "trade": "mechanical",
            },
            {
                "zone_id": "STG-C",
                "zone_name": "East Staging",
                "capacity_sqft": 2000.0,
                "current_usage_sqft": 1900.0,
                "utilization_pct": 95.0,
                "materials": [
                    "Electrical panels",
                    "Cable reels",
                    "Conduit bundles",
                ],
                "trade": "electrical",
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "staging_zones": zones,
                "note": "Mock data",
            },
            indent=2,
        )

    def _headcount(
        self, project_id: str, trade: str | None
    ) -> str:
        today = date.today()
        counts = [
            {
                "date": today.isoformat(),
                "trade": "steel",
                "planned": 20,
                "actual": 18,
                "variance": -2,
                "location": "Building A",
            },
            {
                "date": today.isoformat(),
                "trade": "concrete",
                "planned": 15,
                "actual": 15,
                "variance": 0,
                "location": "Building A",
            },
            {
                "date": today.isoformat(),
                "trade": "electrical",
                "planned": 24,
                "actual": 22,
                "variance": -2,
                "location": "Building A — Levels 2-4",
            },
            {
                "date": today.isoformat(),
                "trade": "mechanical",
                "planned": 18,
                "actual": 20,
                "variance": 2,
                "location": "Building B",
            },
        ]
        if trade:
            counts = [
                c for c in counts if c["trade"] == trade
            ]
        return json.dumps(
            {
                "project_id": project_id,
                "headcount": counts,
                "note": "Mock data",
            },
            indent=2,
        )

    def _permits(self, project_id: str) -> str:
        today = date.today()
        permits = [
            {
                "id": "SP-001",
                "type": "street_closure",
                "status": "active",
                "start_date": (
                    today - timedelta(days=30)
                ).isoformat(),
                "end_date": (
                    today + timedelta(days=60)
                ).isoformat(),
                "conditions": [
                    "Lane closure 7AM-5PM only",
                    "Flaggers required",
                ],
            },
            {
                "id": "SP-002",
                "type": "crane_permit",
                "status": "active",
                "start_date": (
                    today - timedelta(days=60)
                ).isoformat(),
                "end_date": (
                    today + timedelta(days=120)
                ).isoformat(),
                "conditions": [
                    "No lifts over public sidewalk",
                    "Wind speed limit: 30 mph",
                ],
            },
            {
                "id": "SP-003",
                "type": "sidewalk_closure",
                "status": "expiring",
                "start_date": (
                    today - timedelta(days=90)
                ).isoformat(),
                "end_date": (
                    today + timedelta(days=10)
                ).isoformat(),
                "conditions": [
                    "Covered pedestrian walkway required",
                ],
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "site_permits": permits,
                "note": "Mock data",
            },
            indent=2,
        )
