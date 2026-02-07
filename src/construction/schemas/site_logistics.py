"""Pydantic schemas for site logistics management."""

from datetime import date

from pydantic import BaseModel


class CraneScheduleEntry(BaseModel):
    """Crane or hoist schedule entry."""

    crane_id: str
    date: date
    time_slot: str
    trade: str
    activity: str
    weight_tons: float
    duration_hours: float
    status: str  # scheduled/in_progress/completed/cancelled


class StagingPlan(BaseModel):
    """Material staging zone plan."""

    zone_id: str
    zone_name: str
    capacity_sqft: float
    current_usage_sqft: float
    utilization_pct: float
    materials: list[str]
    trade: str | None = None


class SiteHeadcount(BaseModel):
    """Daily site headcount by trade."""

    date: date
    trade: str
    planned: int
    actual: int
    variance: int
    location: str | None = None


class SiteLogisticsReport(BaseModel):
    """Full site logistics report."""

    project_id: str
    crane_schedule: list[CraneScheduleEntry]
    staging: list[StagingPlan]
    headcount: list[SiteHeadcount]
    generated_at: date
