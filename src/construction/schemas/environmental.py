"""Pydantic schemas for environmental and sustainability."""

from datetime import date, datetime

from pydantic import BaseModel


class PermitStatus(BaseModel):
    """Environmental permit status."""

    id: str
    permit_type: str  # SWPPP/air/noise/water/waste
    status: str  # active/expiring/expired/pending
    expiry: date | None = None
    last_inspection: date | None = None
    conditions: list[str]


class LEEDCredit(BaseModel):
    """LEED credit tracking."""

    credit_id: str
    category: str  # energy/water/materials/indoor_quality/innovation
    points: float
    max_points: float
    status: str  # earned/pending/at_risk/not_pursued
    documentation: str | None = None


class CarbonMetric(BaseModel):
    """Carbon emissions tracking."""

    period: str
    scope: str  # scope1/scope2/scope3
    emissions_mt: float
    target_mt: float
    variance_pct: float


class SWPPPCheck(BaseModel):
    """Stormwater Pollution Prevention Plan inspection."""

    date: date
    inspector: str
    findings: list[str]
    corrective_actions: list[str]
    compliant: bool


class EnvironmentalReport(BaseModel):
    """Full environmental compliance report."""

    project_id: str
    permits: list[PermitStatus]
    leed_credits: list[LEEDCredit]
    carbon: list[CarbonMetric]
    generated_at: datetime
