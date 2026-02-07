"""Daily briefing API endpoints."""

from datetime import UTC, date, datetime

from fastapi import APIRouter

from construction.schemas.orchestrator import (
    AccelerationOpportunity,
    DailyBriefOutput,
    QualityGap,
    ThreatSummary,
)

router = APIRouter()

_MOCK_BRIEF = DailyBriefOutput(
    brief_date=date(2025, 2, 3),
    generated_at=datetime(
        2025, 2, 3, 6, 0, tzinfo=UTC
    ),
    top_threats=[
        ThreatSummary(
            rank=1,
            title=(
                "Steel delivery delay risk from"
                " port congestion"
            ),
            agent_source="supply_chain",
            impact="$150K cost, 10-day schedule impact",
            confidence=0.82,
            action_required=(
                "Approve alternative vendor expedite"
            ),
        ),
        ThreatSummary(
            rank=2,
            title="Float erosion on critical path Zone A",
            agent_source="schedule",
            impact="3 days float consumed this week",
            confidence=0.91,
            action_required="Review crew reallocation plan",
        ),
        ThreatSummary(
            rank=3,
            title="Ironworker shortage next week",
            agent_source="workforce",
            impact="6-person gap, productivity at risk",
            confidence=0.78,
            action_required="Contact union hall for dispatch",
        ),
    ],
    quality_gaps=[
        QualityGap(
            rank=1,
            title="Wall thickness deviation at Grid A-3",
            agent_source="compliance",
            severity="major",
            location="Level 2, Grid A-3",
        ),
        QualityGap(
            rank=2,
            title="Concrete strength below spec",
            agent_source="compliance",
            severity="minor",
            location="Level 1, Foundation F-12",
        ),
    ],
    acceleration=AccelerationOpportunity(
        title="Weekend concrete pour for Zone B",
        agent_source="schedule",
        potential_savings_days=3,
        cost=45000,
        description=(
            "Running weekend shift for Zone B pour"
            " could recover 3 days of float"
        ),
    ),
    full_text=(
        "## Daily Brief - February 3, 2025\n\n"
        "Project is tracking 45 days behind baseline."
        " Three key threats require attention today."
    ),
)


@router.get("/daily", response_model=DailyBriefOutput)
async def get_latest_brief():
    """Latest daily brief."""
    return _MOCK_BRIEF


@router.get(
    "/{brief_date}", response_model=DailyBriefOutput
)
async def get_brief_by_date(brief_date: date):
    """Daily brief for a specific date."""
    brief = _MOCK_BRIEF.model_copy()
    brief.brief_date = brief_date
    return brief
