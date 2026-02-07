"""Schedule management API endpoints."""

from datetime import UTC, date, datetime

from fastapi import APIRouter

from construction.schemas.schedule import (
    Activity,
    CriticalPath,
    FloatReport,
    MonteCarloRequest,
    MonteCarloResult,
)

router = APIRouter()


@router.get("/critical-path", response_model=CriticalPath)
async def get_critical_path():
    """Get current critical path."""
    return CriticalPath(
        activities=[
            Activity(
                id="ACT-001",
                external_id="A1010",
                name="Foundation Pour - Zone A",
                start_date=date(2025, 3, 1),
                end_date=date(2025, 3, 15),
                total_float=0.0,
                is_critical=True,
                tier_critical=True,
                predecessors=[],
                successors=["ACT-002"],
            ),
            Activity(
                id="ACT-002",
                external_id="A1020",
                name="Steel Erection - Zone A",
                start_date=date(2025, 3, 16),
                end_date=date(2025, 4, 15),
                total_float=0.0,
                is_critical=True,
                tier_critical=True,
                predecessors=["ACT-001"],
                successors=["ACT-003"],
            ),
        ],
        total_duration_days=120,
        float_summary={"Zone A": 0.0, "Zone B": 5.0},
    )


@router.post("/simulate", response_model=MonteCarloResult)
async def run_simulation(request: MonteCarloRequest):
    """Run Monte Carlo schedule simulation."""
    return MonteCarloResult(
        iterations=request.iterations,
        p50_completion=date(2025, 12, 15),
        p80_completion=date(2026, 1, 10),
        p95_completion=date(2026, 2, 28),
        confidence=0.88,
        float_consumed={"Zone A": 0.45, "Zone B": 0.20},
        histogram=[
            {"month": "2025-12", "probability": 0.50},
            {"month": "2026-01", "probability": 0.30},
            {"month": "2026-02", "probability": 0.15},
            {"month": "2026-03", "probability": 0.05},
        ],
        run_at=datetime.now(UTC),
    )


@router.get(
    "/float-report", response_model=list[FloatReport]
)
async def get_float_report():
    """Get float consumption report."""
    return [
        FloatReport(
            activity_id="ACT-001",
            activity_name="Foundation Pour - Zone A",
            total_float=0.0,
            free_float=0.0,
            status="critical",
        ),
        FloatReport(
            activity_id="ACT-003",
            activity_name="MEP Rough-in - Zone B",
            total_float=5.0,
            free_float=3.0,
            status="healthy",
        ),
    ]
