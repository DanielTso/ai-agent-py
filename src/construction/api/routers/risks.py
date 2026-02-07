"""Risk management API endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter

from construction.schemas.risk import (
    RiskAssessmentRequest,
    RiskAssessmentResponse,
    RiskEvent,
    RiskHeatMap,
    RiskHeatMapCell,
    RiskScore,
)

router = APIRouter()

_MOCK_RISK = RiskEvent(
    id="RISK-001",
    project_id="default-project",
    category="weather",
    description="Hurricane season risk to exterior work",
    risk_score=RiskScore(
        probability=0.35,
        impact_dollars=500000,
        impact_days=14,
        safety_critical=False,
        composite_score=175000,
    ),
    confidence=0.82,
    data_sources=[],
    transparency_log=["Checked NOAA 14-day forecast"],
    status="active",
    created_at=datetime(2025, 1, 15, tzinfo=UTC),
)


@router.get("/", response_model=list[RiskEvent])
async def list_risks():
    """List all risk events."""
    return [_MOCK_RISK]


@router.post("/", response_model=RiskEvent)
async def create_risk(risk: RiskAssessmentRequest):
    """Create a risk event."""
    return _MOCK_RISK


@router.get("/heatmap", response_model=RiskHeatMap)
async def get_heatmap():
    """Get risk heat map."""
    return RiskHeatMap(
        cells=[
            RiskHeatMapCell(
                probability_range="0.3-0.5",
                impact_range="$250k-$500k",
                count=2,
                risk_ids=["RISK-001", "RISK-003"],
            ),
            RiskHeatMapCell(
                probability_range="0.1-0.3",
                impact_range="$100k-$250k",
                count=1,
                risk_ids=["RISK-002"],
            ),
        ]
    )


@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess_risks(request: RiskAssessmentRequest):
    """Trigger a risk assessment run."""
    return RiskAssessmentResponse(
        risks=[_MOCK_RISK],
        heatmap=RiskHeatMap(cells=[]),
        generated_at=datetime.now(UTC),
        confidence=0.85,
    )
