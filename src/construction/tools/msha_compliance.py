"""MSHA compliance tool for contractor checks and violations."""

import json

from ai_agent.tools import Tool


class MshaComplianceTool(Tool):
    """Check MSHA compliance for mining-adjacent construction."""

    name = "msha_compliance"
    description = (
        "Check MSHA compliance including contractor checks,"
        " violation searches, and jurisdiction determination."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "contractor_check",
                        "violation_search",
                        "jurisdiction_check",
                    ],
                    "description": "The MSHA compliance action.",
                },
                "contractor": {
                    "type": "string",
                    "description": "Contractor name to check.",
                },
                "mine_id": {
                    "type": "string",
                    "description": "MSHA mine ID.",
                },
                "location": {
                    "type": "string",
                    "description": "Site location for jurisdiction.",
                },
            },
            "required": ["action"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        try:
            if action == "contractor_check":
                return self._contractor_check(
                    kwargs.get("contractor", "Unknown")
                )
            elif action == "violation_search":
                return self._violation_search(
                    kwargs.get("mine_id")
                )
            elif action == "jurisdiction_check":
                return self._jurisdiction_check(
                    kwargs.get("location", "Unknown")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _contractor_check(self, contractor: str) -> str:
        profile = {
            "contractor": contractor,
            "msha_id": "MSHA-4501234",
            "part_46_training": True,
            "part_48_training": False,
            "violations_last_2y": [
                {
                    "violation_id": "V-2024-0891",
                    "standard": "30 CFR 56.14100(b)",
                    "description": (
                        "Defective braking system on haul truck"
                    ),
                    "type": "S&S",
                    "penalty": 4500.00,
                    "date": "2024-08-15",
                },
            ],
            "fatalities_5y": 0,
            "risk_level": "medium",
        }
        return json.dumps(
            {
                "contractor_profile": profile,
                "note": "Mock data",
            },
            indent=2,
        )

    def _violation_search(
        self, mine_id: str | None
    ) -> str:
        violations = [
            {
                "violation_id": "V-2025-0123",
                "mine_id": mine_id or "M-0012345",
                "standard": "30 CFR 56.12004",
                "description": (
                    "Electrical conductor not properly insulated"
                ),
                "type": "S&S",
                "penalty": 3200.00,
                "date": "2025-01-10",
                "abated": False,
            },
            {
                "violation_id": "V-2024-0456",
                "mine_id": mine_id or "M-0012345",
                "standard": "30 CFR 56.14100(b)",
                "description": "Defective brakes on loader",
                "type": "S&S",
                "penalty": 5000.00,
                "date": "2024-11-22",
                "abated": True,
            },
        ]
        return json.dumps(
            {
                "mine_id": mine_id or "M-0012345",
                "violations": violations,
                "note": "Mock data",
            },
            indent=2,
        )

    def _jurisdiction_check(self, location: str) -> str:
        result = {
            "location": location,
            "msha_jurisdiction": False,
            "osha_jurisdiction": True,
            "rationale": (
                "Site is a commercial construction project."
                " MSHA jurisdiction applies only to mining"
                " operations and directly related activities."
                " However, if the project involves borrow pits"
                " or aggregate extraction, MSHA may assert"
                " jurisdiction over those specific operations."
            ),
            "borrow_pit_present": False,
            "recommendation": (
                "OSHA standards apply. Monitor for any"
                " aggregate extraction that could trigger"
                " MSHA jurisdiction."
            ),
        }
        return json.dumps(
            {
                "jurisdiction": result,
                "note": "Mock data",
            },
            indent=2,
        )
