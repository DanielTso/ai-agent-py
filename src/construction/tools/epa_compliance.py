"""EPA compliance tool for CWA, CAA, RCRA, SWPPP, and NEPA."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class EpaComplianceTool(Tool):
    """Check EPA compliance for construction projects."""

    name = "epa_compliance"
    description = (
        "Check EPA compliance including NPDES permits,"
        " air quality, RCRA hazardous waste, stormwater"
        " SWPPP, and NEPA environmental review status."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "npdes_check",
                        "air_quality_check",
                        "rcra_check",
                        "stormwater_check",
                        "nepa_status",
                    ],
                    "description": "The EPA compliance action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "location": {
                    "type": "string",
                    "description": "Site location or zip code.",
                },
                "permit_id": {
                    "type": "string",
                    "description": "Permit identifier for lookup.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "npdes_check":
                return self._npdes_check(
                    project_id, kwargs.get("permit_id")
                )
            elif action == "air_quality_check":
                return self._air_quality_check(
                    project_id, kwargs.get("location")
                )
            elif action == "rcra_check":
                return self._rcra_check(project_id)
            elif action == "stormwater_check":
                return self._stormwater_check(project_id)
            elif action == "nepa_status":
                return self._nepa_status(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _npdes_check(
        self, project_id: str, permit_id: str | None
    ) -> str:
        today = date.today()
        permits = [
            {
                "permit_id": permit_id or "NPDES-TX-0045123",
                "type": "Construction General Permit",
                "status": "active",
                "effective_date": (
                    today - timedelta(days=180)
                ).isoformat(),
                "expiration_date": (
                    today + timedelta(days=185)
                ).isoformat(),
                "facility": "Metro Data Center — Phase 2",
            },
        ]
        sampling = [
            {
                "parameter": "pH",
                "result": 7.2,
                "unit": "SU",
                "effluent_limit_low": 6.0,
                "effluent_limit_high": 9.0,
                "compliant": True,
            },
            {
                "parameter": "TSS",
                "result": 28.0,
                "unit": "mg/L",
                "effluent_limit": 30.0,
                "compliant": True,
            },
            {
                "parameter": "BOD5",
                "result": 18.5,
                "unit": "mg/L",
                "effluent_limit": 30.0,
                "compliant": True,
            },
            {
                "parameter": "Oil & Grease",
                "result": 16.0,
                "unit": "mg/L",
                "effluent_limit": 15.0,
                "compliant": False,
            },
        ]
        exceedances = [
            s for s in sampling if not s["compliant"]
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "permits": permits,
                "discharge_monitoring": sampling,
                "exceedances": exceedances,
                "compliance_status": (
                    "violation" if exceedances else "compliant"
                ),
                "last_sampling_date": (
                    today - timedelta(days=3)
                ).isoformat(),
                "note": "Mock data",
            },
            indent=2,
        )

    def _air_quality_check(
        self, project_id: str, location: str | None
    ) -> str:
        readings = [
            {
                "parameter": "PM2.5",
                "measured": 11.8,
                "unit": "ug/m3",
                "naaqs_limit": 35.0,
                "compliant": True,
                "source": "ambient monitoring",
            },
            {
                "parameter": "PM10",
                "measured": 142.0,
                "unit": "ug/m3",
                "naaqs_limit": 150.0,
                "compliant": True,
                "source": "site perimeter",
            },
            {
                "parameter": "Fugitive Dust",
                "measured": 165.0,
                "unit": "ug/m3",
                "naaqs_limit": 150.0,
                "compliant": False,
                "source": "unpaved haul road",
            },
        ]
        equipment_emissions = [
            {
                "equipment": "Diesel Generator DG-01",
                "pollutant": "NOx",
                "rate": 2.8,
                "unit": "g/hp-hr",
                "permit_limit": 3.0,
                "compliant": True,
            },
            {
                "equipment": "Concrete Batch Plant",
                "pollutant": "Particulate Matter",
                "rate": 0.04,
                "unit": "lb/ton",
                "permit_limit": 0.05,
                "compliant": True,
            },
        ]
        exceedances = [
            r for r in readings if not r["compliant"]
        ]
        controls = [
            "Water trucks on haul roads (3x daily)",
            "Wind screens at material stockpiles",
            "Track-out controls at site exits",
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "location": location or "Austin, TX 78701",
                "ambient_readings": readings,
                "equipment_emissions": equipment_emissions,
                "aqi_index": 68,
                "exceedances": exceedances,
                "control_measures": controls,
                "recommended_controls": (
                    [
                        "Increase watering frequency on haul road",
                        "Apply chemical dust suppressant",
                    ]
                    if exceedances
                    else []
                ),
                "note": "Mock data",
            },
            indent=2,
        )

    def _rcra_check(self, project_id: str) -> str:
        today = date.today()
        waste_streams = [
            {
                "waste_code": "D001",
                "description": "Ignitable waste — used solvents",
                "quantity_lbs": 220,
                "storage_area": "SAA-01",
                "accumulation_start": (
                    today - timedelta(days=45)
                ).isoformat(),
                "days_in_storage": 45,
                "max_days_allowed": 90,
                "compliant": True,
            },
            {
                "waste_code": "D007",
                "description": (
                    "Chromium-contaminated soil"
                ),
                "quantity_lbs": 1800,
                "storage_area": "SAA-02",
                "accumulation_start": (
                    today - timedelta(days=82)
                ).isoformat(),
                "days_in_storage": 82,
                "max_days_allowed": 90,
                "compliant": True,
            },
        ]
        manifests = [
            {
                "manifest_id": "012345678JJK",
                "waste_code": "D001",
                "transporter": "Clean Haulers Inc.",
                "tsdf": "Eco Disposal Facility",
                "ship_date": (
                    today - timedelta(days=30)
                ).isoformat(),
                "received": True,
            },
        ]
        container_inspections = [
            {
                "area": "SAA-01",
                "last_inspection": (
                    today - timedelta(days=5)
                ).isoformat(),
                "condition": "good",
                "labels_correct": True,
                "closed_properly": True,
            },
            {
                "area": "SAA-02",
                "last_inspection": (
                    today - timedelta(days=5)
                ).isoformat(),
                "condition": "good",
                "labels_correct": True,
                "closed_properly": True,
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "generator_status": "SQG",
                "epa_id": "TXD000123456",
                "waste_streams": waste_streams,
                "manifests": manifests,
                "container_inspections": container_inspections,
                "violations": [],
                "note": "Mock data",
            },
            indent=2,
        )

    def _stormwater_check(self, project_id: str) -> str:
        today = date.today()
        inspection_results = [
            {
                "inspection_id": "SWI-001",
                "date": (
                    today - timedelta(days=7)
                ).isoformat(),
                "inspector": "Lisa Chen, CPESC",
                "type": "routine_weekly",
                "overall_status": "corrective_action_needed",
                "findings": [
                    {
                        "bmp": "Silt Fence SF-12",
                        "status": "damaged",
                        "action_required": (
                            "Repair undermined section"
                        ),
                        "priority": "high",
                    },
                    {
                        "bmp": "Inlet Protection IP-04",
                        "status": "functional",
                        "action_required": None,
                        "priority": None,
                    },
                    {
                        "bmp": "Sediment Basin SB-01",
                        "status": "needs_cleanout",
                        "action_required": (
                            "Basin at 60% capacity — clean out"
                        ),
                        "priority": "medium",
                    },
                ],
            },
        ]
        corrective_actions = [
            {
                "id": "CA-001",
                "finding": "Silt Fence SF-12 undermined",
                "assigned_to": "Earthworks crew",
                "due_date": (
                    today + timedelta(days=2)
                ).isoformat(),
                "status": "in_progress",
            },
        ]
        turbidity = [
            {
                "location": "Outfall 001",
                "ntu_reading": 42.0,
                "benchmark": 280.0,
                "compliant": True,
                "date": (
                    today - timedelta(days=7)
                ).isoformat(),
            },
        ]
        rain_events = [
            {
                "date": (
                    today - timedelta(days=3)
                ).isoformat(),
                "rainfall_inches": 0.75,
                "post_storm_inspection": True,
                "issues_found": False,
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "cgp_permit": "TXR150000",
                "swppp_current": True,
                "stabilization_pct": 45.0,
                "inspection_results": inspection_results,
                "corrective_actions": corrective_actions,
                "turbidity_monitoring": turbidity,
                "rain_events_response": rain_events,
                "note": "Mock data",
            },
            indent=2,
        )

    def _nepa_status(self, project_id: str) -> str:
        today = date.today()
        return json.dumps(
            {
                "project_id": project_id,
                "review_type": "Environmental Assessment",
                "status": "FONSI issued",
                "lead_agency": "U.S. Army Corps of Engineers",
                "filing_date": (
                    today - timedelta(days=120)
                ).isoformat(),
                "decision_date": (
                    today - timedelta(days=30)
                ).isoformat(),
                "findings": [
                    "No significant impact on wetlands",
                    (
                        "Migratory bird survey completed —"
                        " no nesting activity"
                    ),
                    (
                        "Cultural resources Phase I"
                        " — no findings"
                    ),
                ],
                "mitigation_measures": [
                    (
                        "Install turbidity curtain during"
                        " in-water work"
                    ),
                    (
                        "Limit tree clearing to"
                        " Oct 1 — Mar 31 window"
                    ),
                    (
                        "Weekly noise monitoring at"
                        " property boundary"
                    ),
                ],
                "public_comment_period": {
                    "start": (
                        today - timedelta(days=90)
                    ).isoformat(),
                    "end": (
                        today - timedelta(days=60)
                    ).isoformat(),
                    "comments_received": 12,
                    "status": "closed",
                },
                "categorical_exclusion": False,
                "note": "Mock data",
            },
            indent=2,
        )
