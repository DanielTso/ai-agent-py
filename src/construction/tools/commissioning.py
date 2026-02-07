"""Commissioning query tool for IST, punch lists, and turnover."""

import json
from datetime import UTC, date, datetime, timedelta

from ai_agent.tools import Tool


class CommissioningQuery(Tool):
    """Query commissioning data including IST, punch lists, and turnover."""

    name = "commissioning_query"
    description = (
        "Query commissioning and turnover data including"
        " IST sequences, punch lists, turnover packages,"
        " and witness scheduling."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "ist_sequence",
                        "punch_list",
                        "turnover_status",
                        "schedule_witness",
                    ],
                    "description": "The commissioning action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "system": {
                    "type": "string",
                    "description": "System name to filter by.",
                },
                "data": {
                    "type": "object",
                    "description": "Additional data payload.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "ist_sequence":
                return self._ist_sequence(project_id)
            elif action == "punch_list":
                return self._punch_list(project_id)
            elif action == "turnover_status":
                return self._turnover_status(project_id)
            elif action == "schedule_witness":
                return self._schedule_witness(
                    project_id, kwargs.get("data", {})
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _ist_sequence(self, project_id: str) -> str:
        today = date.today()
        tests = [
            {
                "test_id": "IST-001",
                "description": "Generator start-up and load test",
                "prerequisites": [],
                "status": "completed",
                "witness_required": True,
                "witness_scheduled": True,
                "scheduled_date": (
                    today - timedelta(days=5)
                ).isoformat(),
                "notes": "Passed all parameters",
            },
            {
                "test_id": "IST-002",
                "description": (
                    "UPS system integration test"
                ),
                "prerequisites": ["IST-001"],
                "status": "ready",
                "witness_required": True,
                "witness_scheduled": False,
                "scheduled_date": (
                    today + timedelta(days=3)
                ).isoformat(),
                "notes": None,
            },
            {
                "test_id": "IST-003",
                "description": "ATS transfer test",
                "prerequisites": ["IST-001", "IST-002"],
                "status": "blocked",
                "witness_required": True,
                "witness_scheduled": False,
                "scheduled_date": None,
                "notes": (
                    "Blocked: IST-002 not yet completed"
                ),
            },
            {
                "test_id": "IST-004",
                "description": "HVAC controls integration",
                "prerequisites": [],
                "status": "in_progress",
                "witness_required": False,
                "witness_scheduled": False,
                "scheduled_date": today.isoformat(),
                "notes": "Day 2 of 3-day test sequence",
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "ist_sequence": tests,
                "note": "Mock data",
            },
            indent=2,
        )

    def _punch_list(self, project_id: str) -> str:
        now = datetime.now(UTC)
        items = [
            {
                "id": "PL-001",
                "location": "MER-3A",
                "description": (
                    "Panel LP-3A missing breaker labels"
                ),
                "severity": "B",
                "commissioning_impact": True,
                "assigned_to": "ABC Electric",
                "status": "open",
                "created_at": (
                    now - timedelta(days=2)
                ).isoformat(),
            },
            {
                "id": "PL-002",
                "location": "Roof Level",
                "description": "AHU-1 vibration isolators not installed",
                "severity": "A",
                "commissioning_impact": True,
                "assigned_to": "XYZ Mechanical",
                "status": "in_progress",
                "created_at": (
                    now - timedelta(days=5)
                ).isoformat(),
            },
            {
                "id": "PL-003",
                "location": "Lobby",
                "description": "Paint touch-up needed at column C3",
                "severity": "C",
                "commissioning_impact": False,
                "assigned_to": None,
                "status": "open",
                "created_at": (
                    now - timedelta(days=1)
                ).isoformat(),
            },
        ]
        summary = {"A": 1, "B": 1, "C": 1, "D": 0}
        return json.dumps(
            {
                "project_id": project_id,
                "punch_items": items,
                "summary": summary,
                "note": "Mock data",
            },
            indent=2,
        )

    def _turnover_status(self, project_id: str) -> str:
        packages = [
            {
                "id": "TOP-001",
                "package_name": "Electrical Distribution",
                "system": "electrical",
                "required_docs": [
                    "as-builts",
                    "test_reports",
                    "O&M_manuals",
                    "warranty_letters",
                ],
                "received_docs": [
                    "as-builts",
                    "test_reports",
                ],
                "completion_pct": 50.0,
                "status": "incomplete",
            },
            {
                "id": "TOP-002",
                "package_name": "Fire Alarm System",
                "system": "fire_protection",
                "required_docs": [
                    "as-builts",
                    "test_reports",
                    "acceptance_letter",
                ],
                "received_docs": [
                    "as-builts",
                    "test_reports",
                    "acceptance_letter",
                ],
                "completion_pct": 100.0,
                "status": "ready",
            },
            {
                "id": "TOP-003",
                "package_name": "HVAC Controls",
                "system": "mechanical",
                "required_docs": [
                    "as-builts",
                    "sequence_of_operations",
                    "BAS_graphics",
                    "test_reports",
                    "O&M_manuals",
                ],
                "received_docs": ["as-builts"],
                "completion_pct": 20.0,
                "status": "incomplete",
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "turnover_packages": packages,
                "note": "Mock data",
            },
            indent=2,
        )

    def _schedule_witness(
        self, project_id: str, data: dict
    ) -> str:
        test_id = data.get("test_id", "IST-002")
        witness_date = data.get(
            "date",
            (date.today() + timedelta(days=5)).isoformat(),
        )
        return json.dumps(
            {
                "project_id": project_id,
                "test_id": test_id,
                "witness_date": witness_date,
                "status": "scheduled",
                "note": "Mock data — witness scheduled",
            },
            indent=2,
        )
