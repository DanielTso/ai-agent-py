"""Environmental monitoring API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/permits")
async def get_permits():
    """Environmental permits."""
    return [
        {
            "id": "EP-001",
            "permit_type": "SWPPP",
            "description": (
                "Stormwater Pollution Prevention Plan"
            ),
            "status": "active",
            "expiry_date": "2025-12-31",
            "inspector": "EPA Region 4",
            "last_inspection": "2025-01-15",
        },
        {
            "id": "EP-002",
            "permit_type": "Air Quality",
            "description": "Dust control permit",
            "status": "active",
            "expiry_date": "2025-06-30",
            "inspector": "State DEQ",
            "last_inspection": "2025-01-20",
        },
    ]


@router.get("/leed")
async def get_leed_tracking():
    """LEED credit tracking."""
    return {
        "target_level": "Gold",
        "current_points": 52,
        "target_points": 60,
        "categories": [
            {
                "name": "Energy & Atmosphere",
                "earned": 18,
                "possible": 33,
            },
            {
                "name": "Materials & Resources",
                "earned": 8,
                "possible": 13,
            },
            {
                "name": "Water Efficiency",
                "earned": 7,
                "possible": 11,
            },
            {
                "name": "Indoor Environmental Quality",
                "earned": 10,
                "possible": 16,
            },
            {
                "name": "Sustainable Sites",
                "earned": 9,
                "possible": 26,
            },
        ],
    }


@router.get("/carbon")
async def get_carbon_metrics():
    """Carbon footprint metrics."""
    return {
        "total_embodied_co2_tons": 4250,
        "target_co2_tons": 5000,
        "reduction_pct": 15.0,
        "by_material": [
            {"material": "Concrete", "co2_tons": 2100},
            {"material": "Steel", "co2_tons": 1500},
            {"material": "Aluminum", "co2_tons": 350},
            {"material": "Other", "co2_tons": 300},
        ],
        "offset_credits": 200,
    }
