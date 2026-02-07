"""Pydantic models for financial data across construction agents."""

from datetime import date, datetime

from pydantic import BaseModel, Field


class BudgetStatus(BaseModel):
    """Current budget status for a project."""

    project_id: str
    total_budget: float
    spent_to_date: float
    committed: float
    forecast_at_completion: float
    contingency_remaining: float
    variance_pct: float


class EarnedValue(BaseModel):
    """Earned Value Management (EVM) snapshot."""

    snapshot_date: date
    bcws: float = Field(description="Planned Value (PV)")
    bcwp: float = Field(description="Earned Value (EV)")
    acwp: float = Field(description="Actual Cost (AC)")
    cpi: float = Field(description="Cost Performance Index")
    spi: float = Field(description="Schedule Performance Index")
    eac: float = Field(description="Estimate at Completion")
    etc: float = Field(description="Estimate to Complete")
    vac: float = Field(description="Variance at Completion")
    tcpi: float = Field(
        description="To-Complete Performance Index"
    )


class CashFlow(BaseModel):
    """Cash flow data for a single period."""

    period: str
    planned_draw: float
    actual_draw: float
    cumulative_planned: float
    cumulative_actual: float


class ChangeOrder(BaseModel):
    """A change order record."""

    id: str
    co_number: str
    description: str
    cost_impact: float
    schedule_impact_days: int
    status: str  # pending/approved/rejected/executed
    submitted_date: date | None = None
    approved_date: date | None = None


class FinancialReport(BaseModel):
    """Complete financial report for a project."""

    project_id: str
    budget: BudgetStatus
    earned_value: EarnedValue
    cash_flow: list[CashFlow]
    pending_change_orders: list[ChangeOrder]
    generated_at: datetime
    confidence: float = Field(ge=0, le=1)
