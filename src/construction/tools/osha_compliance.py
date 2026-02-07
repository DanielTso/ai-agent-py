"""OSHA compliance tool for 300 log, Focus Four, and standards."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class OshaComplianceTool(Tool):
    """Check OSHA compliance including 300 log and Focus Four."""

    name = "osha_compliance"
    description = (
        "Check OSHA compliance including 300 log,"
        " Focus Four hazards, silica, electrical,"
        " and excavation standards."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "osha_300_log",
                        "focus_four_check",
                        "silica_check",
                        "electrical_check",
                        "excavation_check",
                    ],
                    "description": "The OSHA compliance action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "location": {
                    "type": "string",
                    "description": "Site location to check.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "osha_300_log":
                return self._osha_300_log(project_id)
            elif action == "focus_four_check":
                return self._focus_four_check(project_id)
            elif action == "silica_check":
                return self._silica_check(
                    project_id, kwargs.get("location")
                )
            elif action == "electrical_check":
                return self._electrical_check(project_id)
            elif action == "excavation_check":
                return self._excavation_check(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _osha_300_log(self, project_id: str) -> str:
        today = date.today()
        records = [
            {
                "case_number": "2025-001",
                "employee_name": "John Doe",
                "job_title": "Ironworker",
                "date_of_injury": (
                    today - timedelta(days=45)
                ).isoformat(),
                "description": (
                    "Laceration from sharp metal edge"
                ),
                "classification": "recordable",
                "days_away": 0,
                "days_restricted": 3,
                "death": False,
            },
            {
                "case_number": "2025-002",
                "employee_name": "Jane Smith",
                "job_title": "Electrician",
                "date_of_injury": (
                    today - timedelta(days=20)
                ).isoformat(),
                "description": (
                    "Electrical shock from exposed conductor"
                ),
                "classification": "recordable",
                "days_away": 2,
                "days_restricted": 5,
                "death": False,
            },
            {
                "case_number": "2025-003",
                "employee_name": "Bob Johnson",
                "job_title": "Laborer",
                "date_of_injury": (
                    today - timedelta(days=10)
                ).isoformat(),
                "description": "Twisted ankle on uneven surface",
                "classification": "first_aid",
                "days_away": 0,
                "days_restricted": 0,
                "death": False,
            },
        ]
        summary = {
            "total_recordable": 2,
            "total_dart": 1,
            "total_fatalities": 0,
            "total_hours_worked": 185000,
        }
        return json.dumps(
            {
                "project_id": project_id,
                "osha_300_log": records,
                "summary": summary,
                "note": "Mock data",
            },
            indent=2,
        )

    def _focus_four_check(self, project_id: str) -> str:
        checks = {
            "falls": {
                "status": "warning",
                "findings": [
                    "Guardrail missing at Level 5 east edge",
                    "Floor opening at stairwell B not covered",
                ],
                "standard": "29 CFR 1926.501",
                "recommendations": [
                    "Install guardrail immediately",
                    "Cover floor opening with rated cover",
                ],
            },
            "struck_by": {
                "status": "compliant",
                "findings": [],
                "standard": "29 CFR 1926.602",
                "recommendations": [],
            },
            "caught_in_between": {
                "status": "compliant",
                "findings": [],
                "standard": "29 CFR 1926.652",
                "recommendations": [],
            },
            "electrocution": {
                "status": "critical",
                "findings": [
                    "Exposed wiring in MER-2B without lockout",
                    "GFCI not installed on temporary power panel TP-3",
                ],
                "standard": "29 CFR 1926.405",
                "recommendations": [
                    "Implement LOTO on MER-2B immediately",
                    "Install GFCI protection on TP-3",
                    "Stop work in affected area",
                ],
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "focus_four": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _silica_check(
        self, project_id: str, location: str | None
    ) -> str:
        monitoring = [
            {
                "id": "SIL-001",
                "substance": "respirable crystalline silica",
                "measured_level": 42.0,
                "unit": "ug/m3",
                "osha_pel": 50.0,
                "action_level": 25.0,
                "location": location or "Building A — Level 2",
                "compliant": True,
                "above_action_level": True,
                "controls_in_place": [
                    "Wet cutting methods",
                    "Local exhaust ventilation",
                    "Respiratory protection",
                ],
            },
            {
                "id": "SIL-002",
                "substance": "respirable crystalline silica",
                "measured_level": 55.0,
                "unit": "ug/m3",
                "osha_pel": 50.0,
                "action_level": 25.0,
                "location": "Building B — Exterior",
                "compliant": False,
                "above_action_level": True,
                "controls_in_place": [
                    "Wet cutting methods",
                ],
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "silica_monitoring": monitoring,
                "standard": "29 CFR 1926.1153",
                "note": "Mock data",
            },
            indent=2,
        )

    def _electrical_check(self, project_id: str) -> str:
        checks = {
            "gfci_status": {
                "total_outlets": 48,
                "gfci_protected": 45,
                "non_compliant": 3,
                "locations": [
                    "TP-3 (Level 2)",
                    "TP-7 (Level 4)",
                    "TP-9 (Basement)",
                ],
            },
            "loto_compliance": {
                "active_lockouts": 2,
                "verified": True,
                "findings": [],
            },
            "temporary_power": {
                "panels_inspected": 12,
                "deficiencies": [
                    "TP-3 missing GFCI",
                    "TP-7 cord damage noted",
                ],
            },
            "standard": "29 CFR 1926.405",
        }
        return json.dumps(
            {
                "project_id": project_id,
                "electrical_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _excavation_check(self, project_id: str) -> str:
        checks = {
            "active_excavations": [
                {
                    "id": "EXC-001",
                    "location": "Zone C — Foundation",
                    "depth_ft": 12.0,
                    "soil_type": "Type B",
                    "protection_method": "sloping",
                    "competent_person": "Mike Torres",
                    "daily_inspection": True,
                    "compliant": True,
                },
                {
                    "id": "EXC-002",
                    "location": "Utility Trench — North",
                    "depth_ft": 6.0,
                    "soil_type": "Type C",
                    "protection_method": "trench_box",
                    "competent_person": "Mike Torres",
                    "daily_inspection": True,
                    "compliant": True,
                },
            ],
            "competent_persons_on_site": [
                "Mike Torres — cert valid",
            ],
            "standard": "29 CFR 1926.652",
        }
        return json.dumps(
            {
                "project_id": project_id,
                "excavation_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )
