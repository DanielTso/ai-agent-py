"""Pydantic models for workforce and labor data."""

from datetime import date, datetime

from pydantic import BaseModel


class CrewStatus(BaseModel):
    """Current status of a crew on site."""

    trade: str
    headcount: int
    planned_production: float
    actual_production: float
    productivity_pct: float
    location: str | None = None
    overtime_hours: float


class ProductivityMetric(BaseModel):
    """Productivity tracking for a trade over a period."""

    trade: str
    period: str
    planned_units: float
    actual_units: float
    productivity_index: float
    trend: str  # improving/stable/declining


class CertificationRecord(BaseModel):
    """Worker certification tracking record."""

    worker_id: str
    worker_name: str
    cert_type: str  # OSHA10/OSHA30/BICSI/NETA/competent_person
    issue_date: date | None = None
    expiry_date: date | None = None
    status: str  # valid/expiring_soon/expired


class LaborForecast(BaseModel):
    """Labor availability forecast for a trade."""

    trade: str
    week: str
    required_headcount: int
    available_headcount: int
    gap: int
    critical: bool


class WorkforceReport(BaseModel):
    """Complete workforce report for a project."""

    project_id: str
    crews: list[CrewStatus]
    productivity: list[ProductivityMetric]
    certifications_expiring: list[CertificationRecord]
    labor_forecast: list[LaborForecast]
    generated_at: datetime
