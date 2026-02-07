"""Financial management API endpoints."""

from datetime import date

from fastapi import APIRouter

from construction.schemas.financial import (
    BudgetStatus,
    CashFlow,
    ChangeOrder,
    EarnedValue,
)

router = APIRouter()


@router.get("/evm", response_model=EarnedValue)
async def get_evm():
    """Current earned value metrics."""
    return EarnedValue(
        snapshot_date=date(2025, 2, 1),
        bcws=5000000,
        bcwp=4800000,
        acwp=5100000,
        cpi=0.94,
        spi=0.96,
        eac=21276596,
        etc=16176596,
        vac=-1276596,
        tcpi=1.04,
    )


@router.get("/cashflow", response_model=list[CashFlow])
async def get_cashflow():
    """Cash flow projection."""
    return [
        CashFlow(
            period="2025-01",
            planned_draw=2000000,
            actual_draw=1900000,
            cumulative_planned=2000000,
            cumulative_actual=1900000,
        ),
        CashFlow(
            period="2025-02",
            planned_draw=3000000,
            actual_draw=3200000,
            cumulative_planned=5000000,
            cumulative_actual=5100000,
        ),
    ]


@router.get("/budget", response_model=BudgetStatus)
async def get_budget():
    """Budget status."""
    return BudgetStatus(
        project_id="default-project",
        total_budget=20000000,
        spent_to_date=5100000,
        committed=8500000,
        forecast_at_completion=21276596,
        contingency_remaining=1200000,
        variance_pct=-0.064,
    )


@router.get(
    "/change-orders", response_model=list[ChangeOrder]
)
async def list_change_orders():
    """List change orders."""
    return [
        ChangeOrder(
            id="CO-001",
            co_number="CO-2025-001",
            description=(
                "Additional foundation work due to"
                " unforeseen soil conditions"
            ),
            cost_impact=350000,
            schedule_impact_days=7,
            status="approved",
            submitted_date=date(2025, 1, 20),
            approved_date=date(2025, 1, 28),
        ),
        ChangeOrder(
            id="CO-002",
            co_number="CO-2025-002",
            description="Owner-requested lobby upgrade",
            cost_impact=180000,
            schedule_impact_days=0,
            status="pending",
            submitted_date=date(2025, 2, 5),
        ),
    ]
