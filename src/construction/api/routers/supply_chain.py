"""Supply chain monitoring API endpoints."""

from datetime import UTC, date, datetime

from fastapi import APIRouter

from construction.schemas.supply_chain import (
    AlternativeSourceOption,
    ShipmentTracking,
    SupplyChainAlert,
    VendorStatus,
)

router = APIRouter()

_MOCK_VENDOR = VendorStatus(
    id="V-001",
    name="Acme Steel Corp",
    material="Structural Steel W14x90",
    lead_time_days=45,
    current_status="on_track",
    port_of_origin="Busan, South Korea",
    last_updated=datetime(2025, 2, 1, tzinfo=UTC),
)


@router.get("/vendors", response_model=list[VendorStatus])
async def list_vendors():
    """List vendors with status."""
    return [
        _MOCK_VENDOR,
        VendorStatus(
            id="V-002",
            name="BuildRight Concrete",
            material="Ready-Mix 5000 PSI",
            lead_time_days=3,
            current_status="on_track",
            last_updated=datetime(
                2025, 2, 1, tzinfo=UTC
            ),
        ),
    ]


@router.get(
    "/alerts", response_model=list[SupplyChainAlert]
)
async def get_alerts():
    """Current supply chain alerts."""
    return [
        SupplyChainAlert(
            vendor_id="V-003",
            shipment_id="SHIP-003",
            alert_type="delay",
            severity="warning",
            description=(
                "Curtain wall panels delayed 10 days"
                " due to port congestion"
            ),
            alternatives=[
                AlternativeSourceOption(
                    alt_vendor="GlassTech Inc",
                    cost_delta=15000,
                    schedule_delta_days=-5,
                    recommended=True,
                    confidence=0.78,
                )
            ],
        )
    ]


@router.get(
    "/shipments", response_model=list[ShipmentTracking]
)
async def track_shipments():
    """Track shipments."""
    return [
        ShipmentTracking(
            id="SHIP-001",
            vendor_id="V-001",
            tracking_id="MAEU1234567",
            eta=date(2025, 3, 15),
            original_eta=date(2025, 3, 15),
            delay_days=0,
            status="in_transit",
        )
    ]


@router.post(
    "/alternatives",
    response_model=list[AlternativeSourceOption],
)
async def find_alternatives():
    """Find alternative sourcing options."""
    return [
        AlternativeSourceOption(
            alt_vendor="SteelWorks USA",
            cost_delta=25000,
            schedule_delta_days=-10,
            recommended=True,
            notes="Domestic supplier, faster delivery",
            confidence=0.85,
        ),
        AlternativeSourceOption(
            alt_vendor="Pacific Steel Ltd",
            cost_delta=-5000,
            schedule_delta_days=5,
            recommended=False,
            notes="Cheaper but slower",
            confidence=0.72,
        ),
    ]
