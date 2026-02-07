"""Pydantic models for schedule management and Monte Carlo simulation."""

from datetime import date, datetime

from pydantic import BaseModel, Field


class Activity(BaseModel):
    """A single schedule activity."""

    id: str
    external_id: str
    name: str
    start_date: date | None = None
    end_date: date | None = None
    total_float: float = 0.0
    is_critical: bool = False
    tier_critical: bool = False
    predecessors: list[str] = []
    successors: list[str] = []


class CriticalPath(BaseModel):
    """The critical path through a project schedule."""

    activities: list[Activity] = []
    total_duration_days: int = 0
    float_summary: dict[str, float] = {}


class ScheduleDelta(BaseModel):
    """Describes a schedule change from baseline."""

    baseline_end: date
    projected_end: date
    delta_days: int = 0
    float_consumed: dict[str, float] = {}
    affected_activities: list[str] = []
    description: str = ""


class FloatReport(BaseModel):
    """Float status for a single activity."""

    activity_id: str
    activity_name: str
    total_float: float = 0.0
    free_float: float = 0.0
    status: str = "healthy"  # healthy/warning/critical


class MonteCarloRequest(BaseModel):
    """Request parameters for a Monte Carlo simulation."""

    project_id: str
    iterations: int = 10000
    activity_overrides: dict | None = None
    scenario: str | None = None


class MonteCarloResult(BaseModel):
    """Results from a Monte Carlo schedule simulation."""

    iterations: int
    p50_completion: date
    p80_completion: date
    p95_completion: date
    confidence: float = Field(ge=0, le=1)
    float_consumed: dict[str, float] = {}
    histogram: list[dict] = []
    run_at: datetime
