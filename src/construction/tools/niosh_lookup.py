"""NIOSH lookup tool for RELs, FACE reports, and health hazards."""

import json

from ai_agent.tools import Tool


class NioshLookup(Tool):
    """Look up NIOSH recommended exposure limits and reports."""

    name = "niosh_lookup"
    description = (
        "Look up NIOSH data including recommended"
        " exposure limits (RELs), FACE reports,"
        " and health hazard evaluations."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "rel_lookup",
                        "face_report",
                        "health_hazard",
                    ],
                    "description": "The NIOSH lookup action.",
                },
                "substance": {
                    "type": "string",
                    "description": (
                        "Chemical substance for REL lookup."
                    ),
                },
                "industry": {
                    "type": "string",
                    "description": (
                        "Industry for FACE report search."
                    ),
                },
                "hazard_type": {
                    "type": "string",
                    "description": "Type of health hazard.",
                },
            },
            "required": ["action"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        try:
            if action == "rel_lookup":
                return self._rel_lookup(
                    kwargs.get("substance", "silica")
                )
            elif action == "face_report":
                return self._face_report(
                    kwargs.get("industry", "construction")
                )
            elif action == "health_hazard":
                return self._health_hazard(
                    kwargs.get("hazard_type", "noise")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _rel_lookup(self, substance: str) -> str:
        rels = {
            "silica": {
                "substance": "Crystalline Silica (quartz)",
                "niosh_rel": 0.05,
                "unit": "mg/m3",
                "osha_pel": 0.05,
                "acgih_tlv": 0.025,
                "sampling_time": "TWA 10-hour",
                "health_effects": [
                    "Silicosis",
                    "Lung cancer",
                    "COPD",
                    "Kidney disease",
                ],
                "controls": [
                    "Wet methods for cutting/grinding",
                    "Local exhaust ventilation",
                    "Respiratory protection (APF 10+)",
                    "Exposure monitoring program",
                ],
            },
            "noise": {
                "substance": "Occupational Noise",
                "niosh_rel": 85.0,
                "unit": "dBA (TWA)",
                "osha_pel": 90.0,
                "acgih_tlv": 85.0,
                "sampling_time": "TWA 8-hour",
                "health_effects": [
                    "Noise-induced hearing loss",
                    "Tinnitus",
                ],
                "controls": [
                    "Engineering controls",
                    "Administrative controls",
                    "Hearing protection (NRR 25+)",
                    "Audiometric testing program",
                ],
            },
            "lead": {
                "substance": "Lead (inorganic)",
                "niosh_rel": 0.05,
                "unit": "mg/m3",
                "osha_pel": 0.05,
                "acgih_tlv": 0.05,
                "sampling_time": "TWA 10-hour",
                "health_effects": [
                    "Neurological damage",
                    "Kidney damage",
                    "Reproductive effects",
                ],
                "controls": [
                    "Ventilation",
                    "Wet methods",
                    "Respiratory protection",
                    "Blood lead monitoring",
                ],
            },
        }
        data = rels.get(substance.lower(), rels["silica"])
        return json.dumps(
            {"rel_data": data, "note": "Mock data"},
            indent=2,
        )

    def _face_report(self, industry: str) -> str:
        reports = [
            {
                "report_id": "FACE-2024-01",
                "title": (
                    "Ironworker Dies After Falling"
                    " From Structural Steel"
                ),
                "industry": "construction",
                "date": "2024-06-15",
                "summary": (
                    "A 34-year-old ironworker died after"
                    " falling 42 feet from structural steel."
                    " The worker was not tied off and no"
                    " safety nets were in place."
                ),
                "key_recommendations": [
                    "Ensure 100% tie-off above 6 feet",
                    "Install safety nets for steel erection",
                    "Enforce fall protection plan",
                ],
            },
            {
                "report_id": "FACE-2024-02",
                "title": (
                    "Electrician Electrocuted by Contact"
                    " With Energized Conductor"
                ),
                "industry": "construction",
                "date": "2024-09-20",
                "summary": (
                    "A 45-year-old electrician was"
                    " electrocuted when he contacted an"
                    " energized 480V conductor. LOTO"
                    " procedures were not followed."
                ),
                "key_recommendations": [
                    "Implement LOTO for all electrical work",
                    "Verify de-energization before work",
                    "Use voltage-rated PPE",
                ],
            },
        ]
        return json.dumps(
            {
                "industry": industry,
                "face_reports": reports,
                "note": "Mock data",
            },
            indent=2,
        )

    def _health_hazard(self, hazard_type: str) -> str:
        hazards = {
            "noise": {
                "hazard": "Occupational Noise Exposure",
                "affected_trades": [
                    "Concrete workers",
                    "Steel workers",
                    "Equipment operators",
                ],
                "niosh_threshold": "85 dBA TWA",
                "common_sources": [
                    "Concrete saws (100-110 dBA)",
                    "Jackhammers (95-105 dBA)",
                    "Impact wrenches (90-100 dBA)",
                ],
                "medical_surveillance": [
                    "Baseline audiogram",
                    "Annual audiometric testing",
                    "Standard threshold shift monitoring",
                ],
                "control_hierarchy": [
                    "Elimination: schedule noisy work separately",
                    "Engineering: sound barriers, dampening",
                    "Administrative: rotate workers, limit exposure",
                    "PPE: hearing protection NRR 25+",
                ],
            },
            "heat": {
                "hazard": "Heat Stress",
                "affected_trades": [
                    "All outdoor workers",
                    "Roofers",
                    "Concrete workers",
                ],
                "niosh_threshold": (
                    "WBGT varies by workload"
                ),
                "common_sources": [
                    "Direct sun exposure",
                    "Radiant heat from equipment",
                    "Exertional heat from heavy labor",
                ],
                "medical_surveillance": [
                    "Pre-placement medical evaluation",
                    "Heat acclimatization program",
                    "Buddy system monitoring",
                ],
                "control_hierarchy": [
                    "Elimination: schedule work in cooler hours",
                    "Engineering: shade structures, fans",
                    "Administrative: work/rest cycles, hydration",
                    "PPE: cooling vests",
                ],
            },
        }
        data = hazards.get(
            hazard_type.lower(), hazards["noise"]
        )
        return json.dumps(
            {"health_hazard": data, "note": "Mock data"},
            indent=2,
        )
