"""ICC building codes compliance tool."""

import json

from ai_agent.tools import Tool


class IccCodesTool(Tool):
    """Check ICC building codes including IBC, IFC, IMC, IPC, IECC."""

    name = "icc_codes"
    description = (
        "Check ICC building codes compliance including"
        " IBC, IFC, IMC, IPC, and IECC for"
        " construction projects."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "ibc_check",
                        "ifc_check",
                        "imc_check",
                        "ipc_check",
                        "iecc_check",
                    ],
                    "description": "The ICC code check action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "occupancy_type": {
                    "type": "string",
                    "description": (
                        "Occupancy classification"
                        " (e.g. B, S-1, F-1, I-2)."
                    ),
                },
                "location": {
                    "type": "string",
                    "description": "Building location or zone.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "ibc_check":
                return self._ibc_check(
                    project_id, kwargs.get("occupancy_type")
                )
            elif action == "ifc_check":
                return self._ifc_check(project_id)
            elif action == "imc_check":
                return self._imc_check(project_id)
            elif action == "ipc_check":
                return self._ipc_check(project_id)
            elif action == "iecc_check":
                return self._iecc_check(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _ibc_check(
        self, project_id: str, occupancy_type: str | None
    ) -> str:
        classifications = [
            {
                "zone": "Server Hall A",
                "occupancy_group": "B",
                "occupancy_description": "Business",
                "code_section": "IBC Chapter 3",
                "construction_type": "Type I-A",
                "height_limit_ft": "unlimited",
                "area_limit_sqft": "unlimited",
                "height_area_compliant": True,
            },
            {
                "zone": "Generator Room",
                "occupancy_group": "S-1",
                "occupancy_description": (
                    "Moderate-hazard storage"
                ),
                "code_section": "IBC Chapter 3",
                "construction_type": "Type I-A",
                "height_limit_ft": "unlimited",
                "area_limit_sqft": "unlimited",
                "height_area_compliant": True,
            },
            {
                "zone": "Manufacturing Wing",
                "occupancy_group": "F-1",
                "occupancy_description": (
                    "Moderate-hazard factory"
                ),
                "code_section": "IBC Chapter 3",
                "construction_type": "Type II-B",
                "height_limit_ft": 55,
                "area_limit_sqft": 19000,
                "height_area_compliant": True,
            },
        ]
        if occupancy_type:
            classifications = [
                c
                for c in classifications
                if c["occupancy_group"] == occupancy_type
            ]
        structural = {
            "seismic_design_category": "D",
            "wind_speed_mph": 115,
            "snow_load_psf": 30,
            "code_section": "IBC Chapter 16",
            "compliant": True,
        }
        accessibility = {
            "standard": "ICC A117.1 / ADA",
            "accessible_routes": True,
            "accessible_entrances": True,
            "elevator_access": True,
            "restroom_compliance": True,
            "code_section": "IBC Chapter 11",
            "compliant": True,
        }
        egress = {
            "exit_count": 4,
            "exit_separation_compliant": True,
            "travel_distance_ft": 250,
            "max_travel_distance_ft": 300,
            "illuminated_exit_signs": True,
            "code_section": "IBC Chapter 10",
            "compliant": True,
        }
        fire_resistance = {
            "fire_rating_hours": 2,
            "shaft_enclosures": True,
            "fire_barriers": True,
            "code_section": "IBC Chapter 6",
            "compliant": True,
        }
        return json.dumps(
            {
                "project_id": project_id,
                "occupancy_classification": classifications,
                "construction_type": "Type I-A",
                "height_area_compliance": True,
                "structural_requirements": structural,
                "accessibility_checks": accessibility,
                "means_of_egress": egress,
                "fire_resistance": fire_resistance,
                "code_sections_referenced": [
                    "IBC Chapter 3",
                    "IBC Chapter 5",
                    "IBC Chapter 6",
                    "IBC Chapter 10",
                    "IBC Chapter 11",
                    "IBC Chapter 16",
                ],
                "note": "Mock data",
            },
            indent=2,
        )

    def _ifc_check(self, project_id: str) -> str:
        checks = {
            "fire_access": {
                "status": "compliant",
                "fire_lane_width_ft": 20,
                "fire_lane_clearance_ft": 13.5,
                "aerial_access": True,
                "findings": [],
                "code_section": "IFC Chapter 5",
            },
            "fire_protection_systems": {
                "status": "warning",
                "sprinkler_system": "NFPA 13 wet system",
                "fire_alarm": "addressable with voice",
                "standpipe_system": "Class I",
                "findings": [
                    (
                        "Sprinkler head coverage gap"
                        " in Corridor 3B"
                    ),
                ],
                "code_section": "IFC Chapter 9",
            },
            "hazmat_storage": {
                "status": "compliant",
                "materials_on_site": [
                    "diesel fuel (5000 gal)",
                    "battery electrolyte (200 gal)",
                ],
                "storage_compliant": True,
                "spill_containment": True,
                "findings": [],
                "code_section": "IFC Chapter 50",
            },
            "construction_fire_safety": {
                "status": "compliant",
                "fire_watch_posted": True,
                "hot_work_permits": True,
                "temporary_heating_compliant": True,
                "findings": [],
                "code_section": "IFC Chapter 33",
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "ifc_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _imc_check(self, project_id: str) -> str:
        checks = {
            "ventilation_rates": {
                "status": "compliant",
                "outdoor_air_cfm_per_person": 20,
                "required_cfm_per_person": 15,
                "total_supply_cfm": 45000,
                "exhaust_cfm": 42000,
                "findings": [],
                "code_section": "IMC Chapter 4",
            },
            "equipment_compliance": {
                "status": "compliant",
                "ahu_clearances_met": True,
                "boiler_room_ventilation": True,
                "refrigerant_detection": True,
                "findings": [],
                "code_section": "IMC Chapter 3",
            },
            "ductwork_standards": {
                "status": "warning",
                "material": "galvanized steel",
                "fire_dampers_installed": True,
                "smoke_dampers_installed": True,
                "findings": [
                    (
                        "Duct insulation incomplete"
                        " in mechanical shaft 2"
                    ),
                ],
                "code_section": "IMC Chapter 6",
            },
            "energy_recovery": {
                "status": "compliant",
                "erv_installed": True,
                "effectiveness_percent": 72,
                "required_percent": 50,
                "findings": [],
                "code_section": "IMC Chapter 5",
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "imc_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _ipc_check(self, project_id: str) -> str:
        checks = {
            "fixture_compliance": {
                "status": "compliant",
                "water_closets_required": 12,
                "water_closets_provided": 14,
                "lavatories_required": 8,
                "lavatories_provided": 10,
                "drinking_fountains": 4,
                "findings": [],
                "code_section": "IPC Chapter 4",
            },
            "drainage_system": {
                "status": "compliant",
                "building_drain_size_in": 6,
                "vent_system": "conventional",
                "trap_seals_verified": True,
                "cleanouts_accessible": True,
                "findings": [],
                "code_section": "IPC Chapter 7",
            },
            "water_supply": {
                "status": "warning",
                "service_size_in": 4,
                "pressure_psi": 55,
                "min_pressure_psi": 40,
                "cross_connection_control": True,
                "findings": [
                    (
                        "Pressure reducing valve needed"
                        " at Level 6"
                    ),
                ],
                "code_section": "IPC Chapter 6",
            },
            "backflow_prevention": {
                "status": "compliant",
                "devices_installed": 8,
                "devices_tested": 8,
                "annual_test_current": True,
                "findings": [],
                "code_section": "IPC Chapter 6",
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "ipc_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )

    def _iecc_check(self, project_id: str) -> str:
        checks = {
            "envelope_compliance": {
                "status": "compliant",
                "climate_zone": "4A",
                "wall_r_value": 20,
                "required_wall_r_value": 13,
                "roof_r_value": 30,
                "required_roof_r_value": 25,
                "window_u_factor": 0.32,
                "max_window_u_factor": 0.35,
                "findings": [],
                "code_section": "IECC C402",
            },
            "lighting_compliance": {
                "status": "compliant",
                "lpd_w_per_sqft": 0.82,
                "max_lpd_w_per_sqft": 0.90,
                "automatic_controls": True,
                "daylight_responsive": True,
                "findings": [],
                "code_section": "IECC C405",
            },
            "hvac_efficiency": {
                "status": "warning",
                "cooling_efficiency_eer": 11.0,
                "required_eer": 11.2,
                "heating_efficiency_afue": 0.92,
                "required_afue": 0.90,
                "economizer_installed": True,
                "findings": [
                    (
                        "Cooling EER 11.0 below"
                        " minimum 11.2 for unit RTU-4"
                    ),
                ],
                "code_section": "IECC C403",
            },
            "commissioning_requirements": {
                "status": "compliant",
                "cx_plan_submitted": True,
                "cx_agent_assigned": True,
                "systems_to_commission": [
                    "HVAC",
                    "lighting controls",
                    "building envelope",
                    "domestic hot water",
                ],
                "findings": [],
                "code_section": "IECC C408",
            },
        }
        return json.dumps(
            {
                "project_id": project_id,
                "iecc_compliance": checks,
                "note": "Mock data",
            },
            indent=2,
        )
