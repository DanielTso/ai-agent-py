"""Pydantic schemas for claims and dispute tracking."""

from datetime import date, datetime

from pydantic import BaseModel


class ClaimEventRecord(BaseModel):
    """A claim-related event record."""

    id: str
    event_type: str  # delay/disruption/change/differing_condition/force_majeure
    description: str
    event_date: date
    causation_chain: list[str]
    notice_required: bool
    notice_deadline: date | None = None
    notice_sent: bool
    evidence: list[str]
    responsible_party: str | None = None


class DelayAnalysisResult(BaseModel):
    """Result of a delay analysis."""

    analysis_type: str  # TIA/windows/as_planned_vs_as_built
    affected_activities: list[str]
    critical_delay_days: float
    concurrent_delay_days: float
    responsible_party: str | None = None
    narrative: str


class NoticeRecord(BaseModel):
    """Contract notice tracking."""

    id: str
    notice_type: str
    contract_clause: str
    deadline: date
    sent_date: date | None = None
    recipient: str
    status: str  # pending/sent/acknowledged/expired


class CausationChain(BaseModel):
    """Causation chain analysis."""

    events: list[str]
    links: list[dict]
    root_cause: str | None = None
    contributing_factors: list[str]


class ClaimsReport(BaseModel):
    """Full claims status report."""

    project_id: str
    events: list[ClaimEventRecord]
    notices_due: list[NoticeRecord]
    delay_analyses: list[DelayAnalysisResult]
    generated_at: datetime
