"""Commissioning management API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/ist")
async def get_ist_sequence():
    """IST (Integrated System Testing) sequence status."""
    return [
        {
            "id": "IST-001",
            "system": "HVAC - AHU-1",
            "status": "in_progress",
            "progress_pct": 65,
            "tests_passed": 8,
            "tests_total": 12,
            "next_test": "Supply air balance verification",
        },
        {
            "id": "IST-002",
            "system": "Fire Alarm - Zone 1",
            "status": "pending",
            "progress_pct": 0,
            "tests_passed": 0,
            "tests_total": 15,
            "next_test": "Initiating device verification",
        },
    ]


@router.get("/punch")
async def get_punch_list():
    """Punch list items."""
    return [
        {
            "id": "PL-001",
            "description": "Damper actuator not responding",
            "system": "HVAC",
            "location": "Level 3, Mechanical Room",
            "severity": "major",
            "assigned_to": "MechCo LLC",
            "status": "open",
        },
        {
            "id": "PL-002",
            "description": "Missing fire caulk at penetration",
            "system": "Fire Protection",
            "location": "Level 2, Grid B-4",
            "severity": "critical",
            "assigned_to": "FireStop Inc",
            "status": "in_progress",
        },
    ]


@router.get("/turnover")
async def get_turnover_status():
    """Turnover package status."""
    return [
        {
            "id": "TO-001",
            "system": "HVAC",
            "documents_complete": 12,
            "documents_required": 18,
            "progress_pct": 66.7,
            "status": "in_progress",
            "missing": [
                "TAB report",
                "Sequence of operations",
                "Training records",
            ],
        },
        {
            "id": "TO-002",
            "system": "Electrical",
            "documents_complete": 20,
            "documents_required": 20,
            "progress_pct": 100.0,
            "status": "complete",
            "missing": [],
        },
    ]
