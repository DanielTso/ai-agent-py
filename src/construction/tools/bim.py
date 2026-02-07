"""BIM model query and compliance checking tool."""

import json
from datetime import UTC, datetime

from ai_agent.tools import Tool


class BIMQueryTool(Tool):
    """Query BIM model elements and check compliance."""

    name = "bim_query"
    description = (
        "Query BIM model elements and check compliance"
        " against design specs."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "query_element",
                        "check_compliance",
                        "get_deviations",
                    ],
                    "description": "The BIM action to perform.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "element_id": {
                    "type": "string",
                    "description": "BIM element ID to query.",
                },
                "check_type": {
                    "type": "string",
                    "description": (
                        "Type of compliance check to run."
                    ),
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        element_id = kwargs.get("element_id")
        check_type = kwargs.get("check_type")

        try:
            if action == "query_element":
                return self._query_element(
                    project_id, element_id
                )
            elif action == "check_compliance":
                return self._check_compliance(
                    project_id, check_type
                )
            elif action == "get_deviations":
                return self._get_deviations(project_id)
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _query_element(
        self, project_id: str, element_id: str | None
    ) -> str:
        if not element_id:
            return (
                "Error: element_id is required"
                " for query_element"
            )
        element = {
            "element_id": element_id,
            "element_type": "HVAC_Duct",
            "system": "Cooling Loop A",
            "floor": "Level 3",
            "zone": "Data Hall A",
            "material": "Galvanized Steel",
            "dimensions": {
                "width_mm": 600,
                "height_mm": 400,
                "length_mm": 3000,
            },
            "spec_reference": "ASHRAE 90.1-2019",
            "installation_status": "installed",
        }
        return json.dumps(
            {"project_id": project_id, "element": element},
            indent=2,
        )

    def _check_compliance(
        self, project_id: str, check_type: str | None
    ) -> str:
        now = datetime.now(UTC).isoformat()
        checks = []
        if check_type in (None, "fire_separation"):
            checks.append({
                "id": "CHK-001",
                "project_id": project_id,
                "check_type": "fire_separation",
                "bim_element_id": "WALL-FS-301",
                "measured_value": "1.5 hours",
                "required_value": "2.0 hours",
                "deviation": -0.25,
                "severity": "critical",
                "status": "open",
                "location": "Level 3, Grid B-4",
                "description": (
                    "Fire separation wall rating below"
                    " 2-hour requirement"
                ),
                "created_at": now,
            })
        if check_type in (None, "redundancy_path"):
            checks.append({
                "id": "CHK-002",
                "project_id": project_id,
                "check_type": "redundancy_path",
                "bim_element_id": "PIPE-CL-205",
                "measured_value": "single path",
                "required_value": "dual redundant path",
                "deviation": None,
                "severity": "critical",
                "status": "open",
                "location": "Mechanical Room 2B",
                "description": (
                    "Cooling loop lacks redundant path"
                    " per Tier III requirement"
                ),
                "created_at": now,
            })
        if check_type in (None, "egress"):
            checks.append({
                "id": "CHK-003",
                "project_id": project_id,
                "check_type": "egress",
                "bim_element_id": "DOOR-EG-102",
                "measured_value": "850mm",
                "required_value": "915mm",
                "deviation": -0.071,
                "severity": "major",
                "status": "open",
                "location": "Level 1, Exit B",
                "description": (
                    "Egress door width below minimum"
                    " clearance requirement"
                ),
                "created_at": now,
            })
        return json.dumps(
            {"project_id": project_id, "checks": checks},
            indent=2,
        )

    def _get_deviations(self, project_id: str) -> str:
        deviations = [
            {
                "element_id": "WALL-FS-301",
                "element_type": "Fire_Separation_Wall",
                "deviation_type": "rating_deficiency",
                "measured": "1.5 hours",
                "required": "2.0 hours",
                "visual_url": None,
            },
            {
                "element_id": "PIPE-CL-205",
                "element_type": "Cooling_Pipe",
                "deviation_type": "redundancy_missing",
                "measured": "single path",
                "required": "dual redundant path",
                "visual_url": None,
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "deviations": deviations,
            },
            indent=2,
        )
