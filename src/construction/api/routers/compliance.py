"""Compliance checking API endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter

from construction.schemas.compliance import (
    ComplianceCheck,
    ComplianceReport,
    DeviationTicket,
)

router = APIRouter()

_MOCK_CHECK = ComplianceCheck(
    id="CC-001",
    project_id="default-project",
    check_type="bim_vs_field",
    bim_element_id="WALL-A-101",
    measured_value="4.5 inches",
    required_value="6 inches",
    deviation=1.5,
    severity="major",
    status="open",
    location="Level 2, Grid A-3",
    description="Wall thickness deviation detected",
    created_at=datetime(2025, 2, 1, tzinfo=UTC),
)


@router.get(
    "/tickets", response_model=list[DeviationTicket]
)
async def list_tickets():
    """List compliance deviation tickets."""
    return [
        DeviationTicket(
            id="DT-001",
            compliance_check_id="CC-001",
            title="Wall thickness deviation at A-3",
            description=(
                "BIM model shows 6in wall but field"
                " measurement is 4.5in"
            ),
            severity="major",
            bim_overlay_url=None,
            assigned_to="Field Engineer",
            status="open",
        )
    ]


@router.post("/check", response_model=ComplianceReport)
async def run_compliance_check():
    """Run a compliance check."""
    return ComplianceReport(
        project_id="default-project",
        checks=[_MOCK_CHECK],
        total_open=1,
        critical_count=0,
        generated_at=datetime.now(UTC),
    )


@router.get("/summary")
async def compliance_summary():
    """Compliance summary statistics."""
    return {
        "total_checks": 42,
        "open": 5,
        "in_progress": 3,
        "resolved": 30,
        "accepted": 4,
        "critical": 1,
        "major": 3,
        "minor": 1,
    }
