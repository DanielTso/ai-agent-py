"""Pydantic schemas for commissioning and turnover."""

from datetime import date, datetime

from pydantic import BaseModel


class ISTSequence(BaseModel):
    """Integrated System Test sequence entry."""

    test_id: str
    description: str
    prerequisites: list[str]
    status: str  # pending/ready/in_progress/completed/blocked
    witness_required: bool
    witness_scheduled: bool
    scheduled_date: date | None = None
    notes: str | None = None


class PunchItem(BaseModel):
    """Punch list item for commissioning."""

    id: str
    location: str
    description: str
    severity: str  # A/B/C/D
    commissioning_impact: bool
    assigned_to: str | None = None
    status: str  # open/in_progress/completed/rejected
    created_at: datetime


class TurnoverPackage(BaseModel):
    """System turnover package status."""

    id: str
    package_name: str
    system: str
    required_docs: list[str]
    received_docs: list[str]
    completion_pct: float
    status: str  # incomplete/ready/accepted


class CommissioningReport(BaseModel):
    """Full commissioning status report."""

    project_id: str
    ist_summary: list[ISTSequence]
    punch_summary: dict[str, int]
    turnover_status: list[TurnoverPackage]
    generated_at: datetime
