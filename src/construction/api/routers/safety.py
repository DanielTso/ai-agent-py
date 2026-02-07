"""Safety management API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
async def get_safety_metrics():
    """Safety metrics (TRIR, DART, EMR)."""
    return {
        "trir": 1.8,
        "dart": 0.9,
        "emr": 0.85,
        "days_since_recordable": 45,
        "near_misses_ytd": 12,
        "first_aid_ytd": 8,
        "recordables_ytd": 2,
        "man_hours_ytd": 220000,
    }


@router.get("/osha300")
async def get_osha300():
    """OSHA 300 log."""
    return [
        {
            "case_number": "2025-001",
            "employee": "Worker A",
            "date_of_injury": "2025-01-12",
            "description": "Struck by falling debris",
            "classification": "recordable",
            "days_away": 3,
            "days_restricted": 5,
            "body_part": "Left shoulder",
        },
        {
            "case_number": "2025-002",
            "employee": "Worker B",
            "date_of_injury": "2025-01-28",
            "description": "Slip on wet surface",
            "classification": "first_aid",
            "days_away": 0,
            "days_restricted": 0,
            "body_part": "Right knee",
        },
    ]


@router.get("/inspections")
async def get_inspections():
    """Inspection history."""
    return [
        {
            "id": "INS-001",
            "date": "2025-02-01",
            "inspector": "Safety Manager",
            "area": "Level 3 - Steel Erection",
            "findings": 2,
            "critical_findings": 0,
            "status": "closed",
            "items": [
                {
                    "description": (
                        "Missing guardrail at opening"
                    ),
                    "severity": "major",
                    "corrected": True,
                },
                {
                    "description": (
                        "Incomplete fall protection tie-off"
                    ),
                    "severity": "minor",
                    "corrected": True,
                },
            ],
        },
    ]


@router.get("/readiness-score")
async def get_readiness_score():
    """Inspection readiness score."""
    return {
        "overall_score": 87,
        "categories": [
            {
                "name": "Fall Protection",
                "score": 92,
                "status": "good",
            },
            {
                "name": "Electrical Safety",
                "score": 88,
                "status": "good",
            },
            {
                "name": "Housekeeping",
                "score": 78,
                "status": "needs_improvement",
            },
            {
                "name": "PPE Compliance",
                "score": 95,
                "status": "excellent",
            },
            {
                "name": "Scaffolding",
                "score": 82,
                "status": "good",
            },
        ],
    }


@router.get("/contractors")
async def get_contractor_profiles():
    """Contractor safety profiles."""
    return [
        {
            "contractor": "SteelWorks LLC",
            "emr": 0.78,
            "trir": 1.2,
            "prequalified": True,
            "incidents_ytd": 0,
            "training_compliance_pct": 100,
        },
        {
            "contractor": "MechCo Inc",
            "emr": 0.92,
            "trir": 2.1,
            "prequalified": True,
            "incidents_ytd": 1,
            "training_compliance_pct": 95,
        },
    ]


@router.get("/exposure")
async def get_exposure_data():
    """Exposure monitoring data."""
    return [
        {
            "hazard": "Silica Dust",
            "area": "Level 1 - Concrete Cutting",
            "measurement": 0.035,
            "pel": 0.05,
            "unit": "mg/m3",
            "status": "below_limit",
            "date": "2025-02-01",
        },
        {
            "hazard": "Noise",
            "area": "Level 3 - Steel Erection",
            "measurement": 88,
            "pel": 90,
            "unit": "dBA",
            "status": "approaching_limit",
            "date": "2025-02-01",
        },
    ]
