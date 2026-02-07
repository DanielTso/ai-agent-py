"""Training tracker tool for certifications and compliance."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class TrainingTracker(Tool):
    """Track worker training certifications and gaps."""

    name = "training_tracker"
    description = (
        "Track worker training certifications,"
        " expiring credentials, and training gaps."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "check_certifications",
                        "expiring_soon",
                        "training_gaps",
                    ],
                    "description": "The training action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "worker_id": {
                    "type": "string",
                    "description": "Worker ID to check.",
                },
                "days_ahead": {
                    "type": "integer",
                    "description": (
                        "Days ahead to check for expiring certs."
                    ),
                    "default": 30,
                },
            },
            "required": ["action"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        try:
            if action == "check_certifications":
                return self._check_certifications(
                    kwargs.get("worker_id")
                )
            elif action == "expiring_soon":
                return self._expiring_soon(
                    kwargs.get("project_id", "default"),
                    kwargs.get("days_ahead", 30),
                )
            elif action == "training_gaps":
                return self._training_gaps(
                    kwargs.get("project_id", "default")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _check_certifications(
        self, worker_id: str | None
    ) -> str:
        today = date.today()
        records = [
            {
                "worker_id": "WRK-101",
                "worker_name": "Mike Johnson",
                "training_type": "OSHA30",
                "completion_date": "2022-06-15",
                "expiry": (
                    today + timedelta(days=180)
                ).isoformat(),
                "status": "valid",
            },
            {
                "worker_id": "WRK-101",
                "worker_name": "Mike Johnson",
                "training_type": "competent_person",
                "completion_date": "2024-01-10",
                "expiry": (
                    today + timedelta(days=15)
                ).isoformat(),
                "status": "expiring",
            },
            {
                "worker_id": "WRK-205",
                "worker_name": "Sarah Chen",
                "training_type": "OSHA10",
                "completion_date": "2023-03-20",
                "expiry": None,
                "status": "valid",
            },
            {
                "worker_id": "WRK-312",
                "worker_name": "James Williams",
                "training_type": "first_aid",
                "completion_date": "2022-11-01",
                "expiry": (
                    today - timedelta(days=30)
                ).isoformat(),
                "status": "expired",
            },
            {
                "worker_id": "WRK-408",
                "worker_name": "Ana Rodriguez",
                "training_type": "hazwoper",
                "completion_date": "2023-06-15",
                "expiry": (
                    today + timedelta(days=7)
                ).isoformat(),
                "status": "expiring",
            },
        ]
        if worker_id:
            records = [
                r for r in records
                if r["worker_id"] == worker_id
            ]
        return json.dumps(
            {
                "certifications": records,
                "note": "Mock data",
            },
            indent=2,
        )

    def _expiring_soon(
        self, project_id: str, days_ahead: int
    ) -> str:
        today = date.today()
        expiring = [
            {
                "worker_id": "WRK-101",
                "worker_name": "Mike Johnson",
                "training_type": "competent_person",
                "expiry": (
                    today + timedelta(days=15)
                ).isoformat(),
                "days_until_expiry": 15,
                "impact": (
                    "Cannot serve as competent person"
                    " for excavation operations"
                ),
            },
            {
                "worker_id": "WRK-408",
                "worker_name": "Ana Rodriguez",
                "training_type": "hazwoper",
                "expiry": (
                    today + timedelta(days=7)
                ).isoformat(),
                "days_until_expiry": 7,
                "impact": (
                    "Cannot perform hazardous waste"
                    " operations"
                ),
            },
            {
                "worker_id": "WRK-512",
                "worker_name": "Carlos Mendez",
                "training_type": "MSHA_Part46",
                "expiry": (
                    today + timedelta(days=20)
                ).isoformat(),
                "days_until_expiry": 20,
                "impact": (
                    "Cannot work at aggregate"
                    " extraction areas"
                ),
            },
        ]
        expiring = [
            e for e in expiring
            if e["days_until_expiry"] <= days_ahead
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "days_ahead": days_ahead,
                "expiring_certifications": expiring,
                "note": "Mock data",
            },
            indent=2,
        )

    def _training_gaps(self, project_id: str) -> str:
        gaps = [
            {
                "gap_type": "competent_person_shortage",
                "description": (
                    "Only 1 qualified competent person"
                    " for excavation (need minimum 2)"
                ),
                "affected_activities": [
                    "Foundation excavation",
                    "Utility trenching",
                ],
                "urgency": "high",
                "recommendation": (
                    "Schedule competent person training"
                    " for 2 additional workers"
                ),
            },
            {
                "gap_type": "expired_certification",
                "description": (
                    "3 workers have expired first aid"
                    " certifications"
                ),
                "affected_activities": [
                    "All site activities",
                ],
                "urgency": "medium",
                "recommendation": (
                    "Schedule first aid/CPR refresher"
                    " course within 2 weeks"
                ),
            },
            {
                "gap_type": "missing_training",
                "description": (
                    "5 new hires missing site-specific"
                    " orientation"
                ),
                "affected_activities": [
                    "Cannot access jobsite",
                ],
                "urgency": "critical",
                "recommendation": (
                    "Conduct orientation before next shift"
                ),
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "training_gaps": gaps,
                "note": "Mock data",
            },
            indent=2,
        )
