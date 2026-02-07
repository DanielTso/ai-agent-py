"""Pydantic models for stakeholder communication."""

from datetime import date

from pydantic import BaseModel

from construction.schemas.common import DataSource


class ReportDraft(BaseModel):
    """A draft report for stakeholders."""

    id: str
    report_type: str  # owner_report/monthly_report/weekly_report
    title: str
    body: str
    tone: str  # business/technical/contractual
    data_sources: list[DataSource]
    status: str  # draft/reviewed/sent


class RFIResponse(BaseModel):
    """A response to a Request for Information."""

    id: str
    rfi_number: str
    question: str
    response: str
    references: list[str]
    status: str  # draft/submitted


class SubNotice(BaseModel):
    """A notice to a subcontractor."""

    id: str
    notice_type: str  # delay/change/claim/safety
    recipient: str
    subject: str
    body: str
    contract_clause: str | None = None
    deadline: date | None = None
    status: str  # draft/sent/acknowledged


class OwnerUpdate(BaseModel):
    """A periodic update to the project owner."""

    id: str
    period: str
    executive_summary: str
    key_metrics: dict
    concerns: list[str]
    next_steps: list[str]
