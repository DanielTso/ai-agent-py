"""Hazard analysis tool for JHA, risk assessment, and controls."""

import json

from ai_agent.tools import Tool


class HazardAnalysis(Tool):
    """Generate job hazard analyses and risk assessments."""

    name = "hazard_analysis"
    description = (
        "Generate job hazard analyses, risk assessments,"
        " and hierarchy of controls recommendations."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "generate_jha",
                        "risk_assessment",
                        "hierarchy_of_controls",
                    ],
                    "description": "The hazard analysis action.",
                },
                "activity": {
                    "type": "string",
                    "description": (
                        "The construction activity to analyze."
                    ),
                },
                "location": {
                    "type": "string",
                    "description": "Work location.",
                },
            },
            "required": ["action"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        activity = kwargs.get(
            "activity", "steel_erection"
        )
        try:
            if action == "generate_jha":
                return self._generate_jha(activity)
            elif action == "risk_assessment":
                return self._risk_assessment(
                    activity, kwargs.get("location")
                )
            elif action == "hierarchy_of_controls":
                return self._hierarchy_of_controls(activity)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _generate_jha(self, activity: str) -> str:
        jhas = {
            "steel_erection": [
                {
                    "activity": "Steel beam hoisting",
                    "hazards": [
                        "Falling from height",
                        "Struck by falling steel",
                        "Crane tip-over",
                        "Pinch points during connection",
                    ],
                    "controls": [
                        "100% tie-off with dual-lanyard",
                        "Exclusion zone under lift",
                        "Crane load chart verification",
                        "Tag lines on all loads",
                    ],
                    "hierarchy_of_controls": [
                        "Engineering: safety nets, perimeter cables",
                        "Administrative: lift plan, spotter required",
                        "PPE: harness, hard hat, gloves",
                    ],
                    "ppe_required": [
                        "Full body harness with shock absorber",
                        "Hard hat (Type II)",
                        "Safety glasses",
                        "Steel-toe boots",
                        "Welding gloves",
                    ],
                    "competent_person_required": True,
                },
                {
                    "activity": "Steel bolt-up connections",
                    "hazards": [
                        "Falls from height",
                        "Dropped tools/bolts",
                        "Hand injuries",
                    ],
                    "controls": [
                        "100% tie-off",
                        "Tool lanyards",
                        "Proper wrench selection",
                    ],
                    "hierarchy_of_controls": [
                        "Engineering: bolt baskets, tool trays",
                        "Administrative: tool inventory before/after",
                        "PPE: gloves, tool lanyards",
                    ],
                    "ppe_required": [
                        "Full body harness",
                        "Hard hat",
                        "Safety glasses",
                        "Work gloves",
                    ],
                    "competent_person_required": True,
                },
            ],
            "excavation": [
                {
                    "activity": "Trench excavation",
                    "hazards": [
                        "Cave-in",
                        "Struck by excavator",
                        "Utility strike",
                        "Hazardous atmosphere",
                    ],
                    "controls": [
                        "Shoring/sloping per soil type",
                        "Spotter for equipment",
                        "811 utility locate",
                        "Air monitoring for >4ft depth",
                    ],
                    "hierarchy_of_controls": [
                        "Elimination: trenchless methods",
                        "Engineering: trench box, shoring",
                        "Administrative: competent person inspection",
                        "PPE: hard hat, high-vis vest",
                    ],
                    "ppe_required": [
                        "Hard hat",
                        "High-visibility vest",
                        "Steel-toe boots",
                        "Safety glasses",
                    ],
                    "competent_person_required": True,
                },
            ],
        }
        data = jhas.get(
            activity.lower(), jhas["steel_erection"]
        )
        return json.dumps(
            {
                "activity": activity,
                "jha_entries": data,
                "note": "Mock data",
            },
            indent=2,
        )

    def _risk_assessment(
        self, activity: str, location: str | None
    ) -> str:
        assessment = {
            "activity": activity,
            "location": location or "General site",
            "risk_matrix": [
                {
                    "hazard": "Fall from height",
                    "likelihood": 3,
                    "severity": 5,
                    "risk_score": 15,
                    "risk_level": "high",
                    "residual_risk": 6,
                    "controls_applied": [
                        "Guardrails",
                        "Fall arrest system",
                        "Training",
                    ],
                },
                {
                    "hazard": "Struck by falling object",
                    "likelihood": 2,
                    "severity": 4,
                    "risk_score": 8,
                    "risk_level": "medium",
                    "residual_risk": 4,
                    "controls_applied": [
                        "Exclusion zones",
                        "Tool lanyards",
                        "Barricades",
                    ],
                },
                {
                    "hazard": "Electrocution",
                    "likelihood": 1,
                    "severity": 5,
                    "risk_score": 5,
                    "risk_level": "medium",
                    "residual_risk": 2,
                    "controls_applied": [
                        "LOTO procedures",
                        "GFCI protection",
                        "Qualified personnel only",
                    ],
                },
            ],
            "overall_risk_level": "high",
            "stop_work_threshold": 20,
        }
        return json.dumps(
            {
                "risk_assessment": assessment,
                "note": "Mock data",
            },
            indent=2,
        )

    def _hierarchy_of_controls(
        self, activity: str
    ) -> str:
        controls = {
            "activity": activity,
            "hierarchy": [
                {
                    "level": 1,
                    "type": "Elimination",
                    "description": (
                        "Remove the hazard entirely"
                    ),
                    "examples": [
                        "Prefabricate at ground level",
                        "Use robotic systems",
                    ],
                    "effectiveness": "most_effective",
                },
                {
                    "level": 2,
                    "type": "Substitution",
                    "description": (
                        "Replace with less hazardous option"
                    ),
                    "examples": [
                        "Use lighter materials",
                        "Substitute wet for dry cutting",
                    ],
                    "effectiveness": "highly_effective",
                },
                {
                    "level": 3,
                    "type": "Engineering Controls",
                    "description": (
                        "Isolate people from hazard"
                    ),
                    "examples": [
                        "Guardrails",
                        "Safety nets",
                        "Ventilation systems",
                        "Machine guards",
                    ],
                    "effectiveness": "effective",
                },
                {
                    "level": 4,
                    "type": "Administrative Controls",
                    "description": (
                        "Change the way people work"
                    ),
                    "examples": [
                        "Training programs",
                        "Work procedures",
                        "Warning signs",
                        "Job rotation",
                    ],
                    "effectiveness": "moderately_effective",
                },
                {
                    "level": 5,
                    "type": "PPE",
                    "description": (
                        "Protect worker with equipment"
                    ),
                    "examples": [
                        "Harnesses",
                        "Respirators",
                        "Hard hats",
                        "Safety glasses",
                    ],
                    "effectiveness": "least_effective",
                },
            ],
        }
        return json.dumps(
            {
                "hierarchy_of_controls": controls,
                "note": "Mock data",
            },
            indent=2,
        )
