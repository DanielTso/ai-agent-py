"""Pydantic models for compliance checking and BIM deviation tracking."""

from datetime import date, datetime

from pydantic import BaseModel


class ComplianceCheck(BaseModel):
    """A single compliance check result."""

    id: str
    project_id: str
    check_type: str  # bim_vs_field/code_compliance/redundancy_path/fire_separation/egress
    bim_element_id: str | None = None
    measured_value: str | None = None
    required_value: str | None = None
    deviation: float | None = None
    severity: str = "info"  # info/minor/major/critical
    status: str = "open"  # open/in_progress/resolved/accepted
    location: str | None = None
    description: str | None = None
    created_at: datetime


class DeviationTicket(BaseModel):
    """A ticket raised for a compliance deviation."""

    id: str
    compliance_check_id: str
    title: str
    description: str
    severity: str  # info/minor/major/critical
    bim_overlay_url: str | None = None
    assigned_to: str | None = None
    due_date: date | None = None
    status: str = "open"


class BIMOverlay(BaseModel):
    """BIM overlay data for a deviation visualization."""

    element_id: str
    element_type: str
    deviation_type: str
    measured: str
    required: str
    visual_url: str | None = None


class ComplianceReport(BaseModel):
    """Summary compliance report for a project."""

    project_id: str
    checks: list[ComplianceCheck] = []
    total_open: int = 0
    critical_count: int = 0
    generated_at: datetime
