"""Uptime Institute Tier certification compliance tool."""

import json

from ai_agent.tools import Tool


class TierCertification(Tool):
    """Check Uptime Institute Tier certification compliance."""

    name = "tier_certification"
    description = (
        "Check Uptime Institute Tier certification compliance"
        " including redundancy, concurrent maintainability,"
        " fault tolerance, and certification status."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "tier_requirements",
                        "redundancy_check",
                        "concurrent_maintainability",
                        "fault_tolerance",
                        "certification_status",
                    ],
                    "description": ("The tier certification action."),
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "tier_level": {
                    "type": "string",
                    "description": ("Tier level (I, II, III, IV). Defaults to III."),
                },
                "system": {
                    "type": "string",
                    "enum": [
                        "power",
                        "cooling",
                        "network",
                        "fire_suppression",
                    ],
                    "description": ("Infrastructure system to check."),
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        tier_level = kwargs.get("tier_level", "III")
        system = kwargs.get("system")
        try:
            if action == "tier_requirements":
                return self._tier_requirements(tier_level)
            elif action == "redundancy_check":
                return self._redundancy_check(project_id, tier_level, system)
            elif action == "concurrent_maintainability":
                return self._concurrent_maintainability(project_id, system)
            elif action == "fault_tolerance":
                return self._fault_tolerance(project_id, system)
            elif action == "certification_status":
                return self._certification_status(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _tier_requirements(self, tier_level: str) -> str:
        tiers = {
            "I": {
                "name": "Tier I — Basic Site Infrastructure",
                "redundancy": "N (no redundancy)",
                "uptime": "99.671%",
                "annual_downtime_hours": 28.8,
                "power": {
                    "ups": "Single path, N capacity",
                    "generator": "Optional",
                    "ats": "Not required",
                    "pdu": "Single path",
                },
                "cooling": {
                    "chiller": "N capacity, single path",
                    "crah": "N capacity",
                    "piping": "Single path",
                },
                "network": {
                    "fiber_entry": "Single entry point",
                    "core_switches": "N (single)",
                },
                "fire_suppression": {
                    "detection": "N capacity",
                    "suppression": "N capacity",
                },
            },
            "II": {
                "name": ("Tier II — Redundant Site Infrastructure Components"),
                "redundancy": "N+1 (component redundancy)",
                "uptime": "99.741%",
                "annual_downtime_hours": 22.0,
                "power": {
                    "ups": "N+1 modules, single path",
                    "generator": "N+1",
                    "ats": "Single",
                    "pdu": "Single path",
                },
                "cooling": {
                    "chiller": "N+1",
                    "crah": "N+1",
                    "piping": "Single path",
                },
                "network": {
                    "fiber_entry": "Single entry point",
                    "core_switches": "N+1",
                },
                "fire_suppression": {
                    "detection": "N+1",
                    "suppression": "N+1",
                },
            },
            "III": {
                "name": ("Tier III — Concurrently Maintainable Site Infrastructure"),
                "redundancy": ("N+1 components, 2N distribution"),
                "uptime": "99.982%",
                "annual_downtime_hours": 1.6,
                "power": {
                    "ups": ("N+1 modules, dual distribution paths"),
                    "generator": "N+1",
                    "ats": "2N (dual transfer switches)",
                    "pdu": "2N (dual distribution)",
                },
                "cooling": {
                    "chiller": "N+1 with isolation valves",
                    "crah": ("2N distribution, N+1 components"),
                    "piping": ("2N (dual chilled water loops)"),
                },
                "network": {
                    "fiber_entry": ("Diverse entry (2 paths minimum)"),
                    "core_switches": "2N",
                },
                "fire_suppression": {
                    "detection": "2N (dual detection zones)",
                    "suppression": "N+1",
                },
            },
            "IV": {
                "name": ("Tier IV — Fault Tolerant Site Infrastructure"),
                "redundancy": "2N+1 or 2(N+1)",
                "uptime": "99.995%",
                "annual_downtime_hours": 0.4,
                "power": {
                    "ups": ("2(N+1) — dual active paths, each with N+1"),
                    "generator": ("2N+1 with automatic failover"),
                    "ats": ("2N with automatic fault isolation"),
                    "pdu": ("2N with compartmentalized distribution"),
                },
                "cooling": {
                    "chiller": ("2(N+1) — dual plants with redundancy"),
                    "crah": ("2N with automatic failover"),
                    "piping": ("2N with isolation and compartmentalization"),
                },
                "network": {
                    "fiber_entry": ("Diverse entry (2+ physically separate paths)"),
                    "core_switches": ("2N with automatic failover"),
                },
                "fire_suppression": {
                    "detection": ("2N with cross-zoned verification"),
                    "suppression": ("2N with compartmentalized zones"),
                },
            },
        }
        data = tiers.get(tier_level, tiers["III"])
        return json.dumps(
            {
                "tier_level": tier_level,
                "requirements": data,
                "note": "Mock data",
            },
            indent=2,
        )

    def _redundancy_check(
        self,
        project_id: str,
        tier_level: str,
        system: str | None,
    ) -> str:
        systems = {
            "power": {
                "system": "power",
                "tier_level": tier_level,
                "components": [
                    {
                        "component": "UPS",
                        "required": "N+1",
                        "installed": "3x 500kVA (N+1)",
                        "status": "compliant",
                    },
                    {
                        "component": "Generator",
                        "required": "N+1",
                        "installed": "3x 2MW diesel",
                        "status": "compliant",
                    },
                    {
                        "component": "ATS",
                        "required": "2N",
                        "installed": ("4x ATS (2 per distribution path)"),
                        "status": "compliant",
                    },
                    {
                        "component": "PDU",
                        "required": "2N",
                        "installed": ("Dual PDU feeds to each rack"),
                        "status": "compliant",
                    },
                ],
                "findings": [],
                "deficiencies": [],
            },
            "cooling": {
                "system": "cooling",
                "tier_level": tier_level,
                "components": [
                    {
                        "component": "Chiller",
                        "required": "N+1",
                        "installed": ("4x 400-ton (3+1 redundancy)"),
                        "status": "compliant",
                    },
                    {
                        "component": "CRAH",
                        "required": "2N",
                        "installed": "12 units in A/B config",
                        "status": "compliant",
                    },
                    {
                        "component": "Chilled water piping",
                        "required": "2N",
                        "installed": ("Dual loop with isolation valves"),
                        "status": "warning",
                        "issue": ("Loop B valve V-207 manual only — recommend automatic isolation"),
                    },
                ],
                "findings": [
                    ("Chilled water loop B valve V-207 requires manual isolation"),
                ],
                "deficiencies": [
                    {
                        "id": "DEF-CW-001",
                        "description": ("Valve V-207 on loop B lacks automatic actuation"),
                        "severity": "warning",
                        "recommendation": ("Install motorized actuator on V-207"),
                    },
                ],
            },
            "network": {
                "system": "network",
                "tier_level": tier_level,
                "components": [
                    {
                        "component": "Fiber entry",
                        "required": ("Diverse (2 paths minimum)"),
                        "installed": ("2 diverse paths from separate COs"),
                        "status": "compliant",
                    },
                    {
                        "component": "Core switches",
                        "required": "2N",
                        "installed": ("Dual core switch stack"),
                        "status": "compliant",
                    },
                ],
                "findings": [],
                "deficiencies": [],
            },
            "fire_suppression": {
                "system": "fire_suppression",
                "tier_level": tier_level,
                "components": [
                    {
                        "component": "Detection",
                        "required": "2N",
                        "installed": ("VESDA + spot detection (dual zone)"),
                        "status": "compliant",
                    },
                    {
                        "component": "Suppression",
                        "required": "N+1",
                        "installed": ("FM-200 with reserve cylinder"),
                        "status": "non_compliant",
                        "issue": ("Reserve cylinder pressure below threshold"),
                    },
                ],
                "findings": [
                    ("FM-200 reserve cylinder pressure at 87% — below 95% threshold"),
                ],
                "deficiencies": [
                    {
                        "id": "DEF-FS-001",
                        "description": ("Reserve suppression cylinder undercharged"),
                        "severity": "non_compliant",
                        "recommendation": ("Recharge or replace reserve FM-200 cylinder"),
                    },
                ],
            },
        }
        if system:
            result = systems.get(system, {})
            checks = {system: result} if result else {}
        else:
            checks = systems
        overall = "compliant"
        for sys_data in checks.values():
            if sys_data.get("deficiencies"):
                for d in sys_data["deficiencies"]:
                    if d["severity"] == "non_compliant":
                        overall = "non_compliant"
                        break
                    if d["severity"] == "warning":
                        overall = "warning"
            if overall == "non_compliant":
                break
        return json.dumps(
            {
                "project_id": project_id,
                "tier_level": tier_level,
                "overall_status": overall,
                "systems": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _concurrent_maintainability(
        self,
        project_id: str,
        system: str | None,
    ) -> str:
        systems = {
            "power": {
                "system": "power",
                "concurrently_maintainable": True,
                "components": {
                    "ups": {
                        "can_maintain_without_load_transfer": True,
                        "maintenance_path": (
                            "Isolate UPS module via"
                            " static bypass, load served"
                            " by remaining N modules"
                        ),
                        "isolation_points": [
                            "UPS input breaker",
                            "UPS output breaker",
                            "Static bypass switch",
                        ],
                        "bypass_capability": True,
                    },
                    "generator": {
                        "can_maintain_without_load_transfer": True,
                        "maintenance_path": ("Isolate generator via ATS, N+1 provides coverage"),
                        "isolation_points": [
                            "Generator output breaker",
                            "ATS transfer mechanism",
                        ],
                        "bypass_capability": True,
                    },
                    "ats": {
                        "can_maintain_without_load_transfer": True,
                        "maintenance_path": ("Use alternate distribution path during ATS service"),
                        "isolation_points": [
                            "ATS input A breaker",
                            "ATS input B breaker",
                            "ATS output breaker",
                        ],
                        "bypass_capability": True,
                    },
                },
                "findings": [],
            },
            "cooling": {
                "system": "cooling",
                "concurrently_maintainable": True,
                "components": {
                    "chiller": {
                        "can_maintain_without_impact": True,
                        "maintenance_path": ("Isolate chiller via valves, N+1 spare serves load"),
                        "isolation_points": [
                            "Chiller supply valve",
                            "Chiller return valve",
                            "Electrical disconnect",
                        ],
                        "bypass_capability": True,
                    },
                    "crah": {
                        "can_maintain_without_impact": True,
                        "maintenance_path": (
                            "Isolate CRAH unit, redundant unit in same zone serves load"
                        ),
                        "isolation_points": [
                            "CRAH supply valve",
                            "CRAH return valve",
                            "Electrical disconnect",
                        ],
                        "bypass_capability": True,
                    },
                },
                "findings": [],
            },
        }
        if system:
            result = systems.get(system, {})
            checks = {system: result} if result else {}
        else:
            checks = systems
        all_maintainable = all(s.get("concurrently_maintainable", False) for s in checks.values())
        return json.dumps(
            {
                "project_id": project_id,
                "tier_iii_concurrent_maintainability": (all_maintainable),
                "systems": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _fault_tolerance(
        self,
        project_id: str,
        system: str | None,
    ) -> str:
        systems = {
            "power": {
                "system": "power",
                "fault_tolerant": True,
                "single_point_of_failure_analysis": {
                    "ups": {
                        "dual_active_paths": True,
                        "automatic_fault_isolation": True,
                        "transfer_time_ms": 10,
                        "max_allowed_ms": 12,
                        "status": "pass",
                    },
                    "generator": {
                        "dual_active_paths": True,
                        "automatic_fault_isolation": True,
                        "auto_start_time_seconds": 10,
                        "status": "pass",
                    },
                    "distribution": {
                        "compartmentalized": True,
                        "fire_rated_separation": True,
                        "status": "pass",
                    },
                },
                "automatic_response": {
                    "ups_failure": ("Automatic transfer to alternate path in <10ms"),
                    "generator_failure": ("Alternate generator auto-starts within 10s"),
                    "utility_loss": ("UPS sustains load, generators start within 10s"),
                },
                "findings": [],
            },
            "cooling": {
                "system": "cooling",
                "fault_tolerant": False,
                "single_point_of_failure_analysis": {
                    "chiller_plant": {
                        "no_single_point_of_failure": True,
                        "compartmentalized": True,
                        "auto_failover": True,
                        "status": "pass",
                    },
                    "distribution": {
                        "no_single_point_of_failure": False,
                        "compartmentalized": True,
                        "auto_failover": True,
                        "status": "fail",
                        "issue": (
                            "Valve V-207 requires manual"
                            " operation — single point"
                            " of failure in loop B"
                        ),
                    },
                },
                "automatic_response": {
                    "chiller_failure": ("Standby chiller auto-starts within 60s"),
                    "crah_failure": ("Redundant CRAH increases output automatically"),
                },
                "findings": [
                    ("Cooling distribution has single point of failure at valve V-207"),
                ],
            },
        }
        if system:
            result = systems.get(system, {})
            checks = {system: result} if result else {}
        else:
            checks = systems
        all_tolerant = all(s.get("fault_tolerant", False) for s in checks.values())
        return json.dumps(
            {
                "project_id": project_id,
                "tier_iv_fault_tolerant": all_tolerant,
                "systems": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _certification_status(self, project_id: str) -> str:
        return json.dumps(
            {
                "project_id": project_id,
                "target_tier": "III",
                "design_certification": {
                    "status": "approved",
                    "score": 92,
                    "date": "2025-03-15",
                    "findings": [
                        ("Minor: cooling valve V-207 automation recommended"),
                    ],
                },
                "construction_certification": {
                    "status": "in_progress",
                    "score": 78,
                    "expected_completion": "2025-09-01",
                    "findings": [
                        ("Fire suppression reserve cylinder needs recharge"),
                        ("Generator fuel system test pending"),
                    ],
                },
                "operational_sustainability": {
                    "status": "not_started",
                    "score": None,
                    "prerequisite": ("Construction certification must be completed first"),
                    "findings": [],
                },
                "note": "Mock data",
            },
            indent=2,
        )
