"""Supply chain monitoring tool."""

import json
from datetime import UTC, date, datetime, timedelta

from ai_agent.tools import Tool


class SupplyChainMonitor(Tool):
    """Monitor vendor status, shipments, and alternative sources."""

    name = "supply_chain_monitor"
    description = (
        "Monitor vendor status, track shipments, and find"
        " alternative sources for construction materials."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "vendor_status",
                        "track_shipment",
                        "find_alternatives",
                    ],
                    "description": "The action to perform",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project ID",
                },
                "vendor_id": {
                    "type": "string",
                    "description": "Vendor ID to query",
                },
                "shipment_id": {
                    "type": "string",
                    "description": "Shipment ID for tracking",
                },
                "material": {
                    "type": "string",
                    "description": "Material type for alternatives",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "vendor_status":
                return self._vendor_status(
                    project_id, kwargs.get("vendor_id")
                )
            elif action == "track_shipment":
                return self._track_shipment(
                    project_id, kwargs.get("shipment_id")
                )
            elif action == "find_alternatives":
                return self._find_alternatives(
                    project_id, kwargs.get("material")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error in supply chain monitor: {exc}"

    def _vendor_status(
        self, project_id: str, vendor_id: str | None
    ) -> str:
        now = datetime.now(UTC).isoformat()
        vendors = [
            {
                "id": "VND-001",
                "name": "Pacific Steel Corp",
                "material": "structural_steel",
                "lead_time_days": 90,
                "current_status": "delayed",
                "port_of_origin": "Shanghai",
                "last_updated": now,
            },
            {
                "id": "VND-002",
                "name": "Gulf Concrete Supply",
                "material": "ready_mix_concrete",
                "lead_time_days": 3,
                "current_status": "on_track",
                "port_of_origin": None,
                "last_updated": now,
            },
            {
                "id": "VND-003",
                "name": "ElectroPro Systems",
                "material": "electrical_switchgear",
                "lead_time_days": 120,
                "current_status": "at_risk",
                "port_of_origin": "Busan",
                "last_updated": now,
            },
            {
                "id": "VND-004",
                "name": "NorthStar HVAC",
                "material": "hvac_units",
                "lead_time_days": 60,
                "current_status": "on_track",
                "port_of_origin": None,
                "last_updated": now,
            },
        ]
        if vendor_id:
            vendors = [v for v in vendors if v["id"] == vendor_id]
        return json.dumps({"vendors": vendors}, indent=2)

    def _track_shipment(
        self, project_id: str, shipment_id: str | None
    ) -> str:
        today = date.today()
        shipments = [
            {
                "id": "SHP-001",
                "vendor_id": "VND-001",
                "tracking_id": "MAEU1234567",
                "eta": (today + timedelta(days=21)).isoformat(),
                "original_eta": (today + timedelta(days=14)).isoformat(),
                "delay_days": 7,
                "delay_reason": "Port congestion at Shanghai",
                "status": "in_transit",
                "milestones": [
                    {
                        "description": "Departed origin port",
                        "timestamp": (
                            datetime.now(UTC) - timedelta(days=10)
                        ).isoformat(),
                        "location": "Shanghai, CN",
                    },
                    {
                        "description": "Transshipment at Busan",
                        "timestamp": (
                            datetime.now(UTC) - timedelta(days=5)
                        ).isoformat(),
                        "location": "Busan, KR",
                    },
                ],
            },
            {
                "id": "SHP-002",
                "vendor_id": "VND-003",
                "tracking_id": "COSCO9876543",
                "eta": (today + timedelta(days=45)).isoformat(),
                "original_eta": (today + timedelta(days=40)).isoformat(),
                "delay_days": 5,
                "delay_reason": "Customs hold at origin",
                "status": "at_origin_port",
                "milestones": [
                    {
                        "description": "Cargo received at port",
                        "timestamp": (
                            datetime.now(UTC) - timedelta(days=3)
                        ).isoformat(),
                        "location": "Busan, KR",
                    },
                ],
            },
        ]
        if shipment_id:
            shipments = [
                s for s in shipments if s["id"] == shipment_id
            ]
        return json.dumps({"shipments": shipments}, indent=2)

    def _find_alternatives(
        self, project_id: str, material: str | None
    ) -> str:
        if not material:
            return "Error: material is required for find_alternatives"

        alternatives = [
            {
                "alt_vendor": "Nucor Steel Inc",
                "cost_delta": 45000.0,
                "schedule_delta_days": -10,
                "recommended": True,
                "notes": (
                    "Domestic supplier, shorter lead time."
                    " Higher unit cost but avoids shipping delays."
                ),
                "confidence": 0.85,
            },
            {
                "alt_vendor": "ArcelorMittal USA",
                "cost_delta": 30000.0,
                "schedule_delta_days": -5,
                "recommended": False,
                "notes": (
                    "Partial inventory available. May need"
                    " split delivery."
                ),
                "confidence": 0.70,
            },
            {
                "alt_vendor": "JSW Steel (India)",
                "cost_delta": -15000.0,
                "schedule_delta_days": 10,
                "recommended": False,
                "notes": (
                    "Lower cost but longer lead time."
                    " Only viable if schedule permits."
                ),
                "confidence": 0.60,
            },
        ]
        return json.dumps(
            {
                "material": material,
                "alternatives": alternatives,
                "note": "Mock data — production integrates real vendor DB",
            },
            indent=2,
        )
