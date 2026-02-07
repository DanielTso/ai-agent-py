"""Claims and dispute management API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/timeline")
async def get_claims_timeline():
    """Claims timeline."""
    return [
        {
            "id": "CLM-001",
            "title": "Differing site conditions - Zone A",
            "type": "differing_conditions",
            "amount": 350000,
            "filed_date": "2025-01-15",
            "status": "under_review",
            "milestones": [
                {
                    "date": "2025-01-10",
                    "event": "Notice of claim filed",
                },
                {
                    "date": "2025-01-15",
                    "event": "Supporting docs submitted",
                },
                {
                    "date": "2025-02-01",
                    "event": "Owner review in progress",
                },
            ],
        },
    ]


@router.get("/notices")
async def get_notices():
    """Notice tracking."""
    return [
        {
            "id": "NOT-001",
            "notice_type": "delay",
            "from_party": "GC",
            "to_party": "Owner",
            "subject": (
                "Weather delay notice - January storms"
            ),
            "sent_date": "2025-01-20",
            "response_due": "2025-02-03",
            "status": "awaiting_response",
        },
        {
            "id": "NOT-002",
            "notice_type": "change",
            "from_party": "GC",
            "to_party": "SubA",
            "subject": "Scope change - MEP reroute",
            "sent_date": "2025-01-25",
            "response_due": "2025-02-08",
            "status": "acknowledged",
        },
    ]


@router.get("/delay-analysis")
async def get_delay_analysis():
    """Delay analysis results."""
    return {
        "method": "time_impact_analysis",
        "baseline_completion": "2025-12-01",
        "projected_completion": "2026-01-15",
        "total_delay_days": 45,
        "excusable_days": 30,
        "non_excusable_days": 15,
        "compensable_days": 20,
        "delay_events": [
            {
                "id": "DE-001",
                "description": "Unforeseen rock removal",
                "delay_days": 14,
                "excusable": True,
                "compensable": True,
            },
            {
                "id": "DE-002",
                "description": "Abnormal rainfall January",
                "delay_days": 10,
                "excusable": True,
                "compensable": False,
            },
            {
                "id": "DE-003",
                "description": (
                    "Late submittal turnaround"
                ),
                "delay_days": 7,
                "excusable": False,
                "compensable": False,
            },
        ],
    }
