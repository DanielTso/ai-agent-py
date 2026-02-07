"""NFPA/NEC compliance tool for fire protection and electrical code."""

import json

from ai_agent.tools import Tool


class NfpaComplianceTool(Tool):
    """Check NFPA and NEC compliance for construction projects."""

    name = "nfpa_compliance"
    description = (
        "Check NFPA and NEC compliance including fire"
        " protection, life safety, sprinkler/alarm systems,"
        " egress, and National Electrical Code articles."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "fire_protection_check",
                        "nec_article_check",
                        "life_safety_check",
                        "sprinkler_alarm_check",
                        "egress_check",
                    ],
                    "description": "The NFPA/NEC compliance action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "location": {
                    "type": "string",
                    "description": "Site location to check.",
                },
                "article_number": {
                    "type": "string",
                    "description": "NEC article number to check.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "fire_protection_check":
                return self._fire_protection_check(project_id)
            elif action == "nec_article_check":
                return self._nec_article_check(
                    project_id, kwargs.get("article_number")
                )
            elif action == "life_safety_check":
                return self._life_safety_check(project_id)
            elif action == "sprinkler_alarm_check":
                return self._sprinkler_alarm_check(project_id)
            elif action == "egress_check":
                return self._egress_check(
                    project_id, kwargs.get("location")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _fire_protection_check(self, project_id: str) -> str:
        checks = {
            "fire_barriers": {
                "status": "warning",
                "findings": [
                    "2-hour fire barrier at Level 3 MER"
                    " missing firestop at pipe penetration",
                    "Smoke barrier at corridor 2B has"
                    " unsealed cable tray opening",
                ],
                "standard": "NFPA 101 Section 8.3",
            },
            "fire_dampers": {
                "status": "compliant",
                "findings": [],
                "standard": "NFPA 80 Section 19.5",
            },
            "firestop_systems": {
                "status": "critical",
                "findings": [
                    "12 penetrations in 2-hour fire wall"
                    " at data center lack UL-listed firestop",
                    "Through-penetration firestop at"
                    " electrical room not per listing",
                ],
                "standard": "NFPA 101 Section 8.3.5",
                "recommendations": [
                    "Install UL-listed firestop systems"
                    " at all rated wall penetrations",
                    "Submit firestop special inspection"
                    " report per NFPA 101",
                ],
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "fire_protection": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _nec_article_check(
        self, project_id: str, article_number: str | None
    ) -> str:
        article = article_number or "210"
        checks = {
            "conductor_sizing": {
                "status": "warning",
                "findings": [
                    "Branch circuit 2B-14 uses #14 AWG"
                    " for 20A circuit — requires #12 AWG",
                ],
                "standard": f"NFPA 70 (NEC) Article {article}",
                "nec_articles": ["210", "220"],
            },
            "overcurrent_protection": {
                "status": "compliant",
                "findings": [],
                "standard": "NFPA 70 (NEC) Article 240",
                "nec_articles": ["240"],
            },
            "grounding": {
                "status": "critical",
                "findings": [
                    "Equipment grounding conductor missing"
                    " at data center PDU-3",
                    "Grounding electrode system not"
                    " bonded per Article 250.50",
                ],
                "standard": "NFPA 70 (NEC) Article 250",
                "nec_articles": ["250"],
                "recommendations": [
                    "Install equipment grounding conductor"
                    " at PDU-3 per NEC 250.118",
                    "Complete grounding electrode bonding"
                    " per NEC 250.50",
                ],
            },
            "emergency_systems": {
                "status": "compliant",
                "findings": [],
                "standard": "NFPA 70 (NEC) Articles 700/701",
                "nec_articles": ["700", "701"],
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "nec_compliance": checks,
                "article_checked": article,
                "note": "Mock data",
            },
            indent=2,
        )

    def _life_safety_check(self, project_id: str) -> str:
        checks = {
            "occupant_load": {
                "floor": "Level 2",
                "calculated_load": 480,
                "design_capacity": 500,
                "compliant": True,
                "standard": "NFPA 101 Section 7.3",
            },
            "exit_capacity": {
                "required_exits": 3,
                "provided_exits": 3,
                "exit_width_total_in": 132,
                "required_width_in": 120,
                "compliant": True,
                "standard": "NFPA 101 Section 7.3.3",
            },
            "travel_distance": {
                "status": "warning",
                "max_travel_ft": 275,
                "allowed_ft": 250,
                "location": "Level 2 east wing to Stair B",
                "compliant": False,
                "standard": "NFPA 101 Section 7.6",
                "recommendations": [
                    "Add intermediate exit or reduce"
                    " travel distance below 250 ft",
                ],
            },
            "exit_signs": {
                "total_required": 24,
                "installed": 22,
                "compliant": False,
                "missing_locations": [
                    "Corridor 2C junction",
                    "Stair D entry Level 3",
                ],
                "standard": "NFPA 101 Section 7.10",
            },
            "emergency_lighting": {
                "status": "compliant",
                "battery_backup_tested": True,
                "last_90min_test": "2025-11-15",
                "standard": "NFPA 101 Section 7.9",
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "life_safety": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _sprinkler_alarm_check(self, project_id: str) -> str:
        checks = {
            "sprinkler_coverage": {
                "status": "warning",
                "system_type": "wet pipe",
                "design_standard": "NFPA 13",
                "areas_inspected": 12,
                "deficiencies": [
                    "Obstructed sprinkler head at"
                    " server room SR-2 (duct blockage)",
                    "Spare sprinkler cabinet missing"
                    " on Level 4",
                ],
                "standard": "NFPA 13 Section 8.5",
            },
            "water_supply": {
                "status": "compliant",
                "static_psi": 85,
                "residual_psi": 65,
                "flow_gpm": 750,
                "required_gpm": 600,
                "standard": "NFPA 13 Section 23.1",
            },
            "fire_alarm": {
                "status": "critical",
                "panel_type": "addressable",
                "zones_programmed": 18,
                "zones_verified": 15,
                "deficiencies": [
                    "Zones 16-18 (Level 4) not yet"
                    " programmed or verified",
                    "Duct detector at AHU-3 not"
                    " connected to alarm panel",
                ],
                "standard": "NFPA 72 Section 23.8",
                "recommendations": [
                    "Complete zone programming for"
                    " Level 4 before occupancy",
                    "Connect AHU-3 duct detector"
                    " to fire alarm panel",
                ],
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "sprinkler_alarm": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _egress_check(
        self, project_id: str, location: str | None
    ) -> str:
        loc = location or "Level 2 — Main Corridor"
        checks = {
            "corridor_width": {
                "location": loc,
                "measured_in": 48,
                "required_in": 44,
                "compliant": True,
                "standard": "NFPA 101 Section 7.3.4",
            },
            "door_swing": {
                "status": "warning",
                "findings": [
                    "Door at Stair C Level 2 swings"
                    " against egress direction",
                ],
                "standard": "NFPA 101 Section 7.2.1.4",
                "recommendations": [
                    "Reverse door swing at Stair C"
                    " to open in direction of egress",
                ],
            },
            "exit_access": {
                "status": "compliant",
                "dead_end_corridors": 0,
                "max_dead_end_ft": 0,
                "allowed_dead_end_ft": 20,
                "standard": "NFPA 101 Section 7.5.1",
            },
            "exit_discharge": {
                "status": "compliant",
                "discharges_to_public_way": True,
                "path_clear": True,
                "standard": "NFPA 101 Section 7.7",
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "egress_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )
