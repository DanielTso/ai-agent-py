"""Site logistics management API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/crane")
async def get_crane_schedule():
    """Crane schedule."""
    return [
        {
            "id": "CR-001",
            "crane_id": "Tower Crane TC-1",
            "date": "2025-02-03",
            "time_slots": [
                {
                    "start": "07:00",
                    "end": "10:00",
                    "trade": "Ironworkers",
                    "description": "Steel erection L3",
                },
                {
                    "start": "10:30",
                    "end": "12:00",
                    "trade": "Concrete",
                    "description": "Bucket pour L2",
                },
                {
                    "start": "13:00",
                    "end": "15:30",
                    "trade": "MEP",
                    "description": "AHU lift L4",
                },
            ],
        },
    ]


@router.get("/staging")
async def get_staging_zones():
    """Staging zone status."""
    return [
        {
            "id": "SZ-001",
            "zone": "North Laydown",
            "capacity_pct": 75,
            "current_materials": [
                "Structural steel - 40 tons",
                "Rebar bundles - 200 pcs",
            ],
            "reserved_until": "2025-02-10",
            "status": "active",
        },
        {
            "id": "SZ-002",
            "zone": "South Staging",
            "capacity_pct": 30,
            "current_materials": [
                "Drywall - 500 sheets",
            ],
            "reserved_until": "2025-02-15",
            "status": "active",
        },
    ]


@router.get("/headcount")
async def get_site_headcount():
    """Site headcount by trade."""
    return {
        "date": "2025-02-03",
        "total": 156,
        "by_trade": [
            {"trade": "Ironworkers", "count": 24},
            {"trade": "Electricians", "count": 18},
            {"trade": "Plumbers", "count": 14},
            {"trade": "Concrete", "count": 20},
            {"trade": "Carpenters", "count": 16},
            {"trade": "Laborers", "count": 32},
            {"trade": "MEP", "count": 22},
            {"trade": "Supervision", "count": 10},
        ],
    }
