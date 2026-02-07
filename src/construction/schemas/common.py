"""Shared Pydantic models used across construction agents."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DataSource(BaseModel):
    """Describes where data came from and its reliability."""

    source_type: str  # "api", "database", "document", "sensor", "manual"
    source_name: str  # "portcast_api", "primavera_p6", etc.
    retrieved_at: datetime
    confidence: float = Field(ge=0, le=1)


class ConfidenceScore(BaseModel):
    """A confidence value with supporting factors."""

    value: float = Field(ge=0, le=1)
    factors: list[str] = []
    methodology: str = ""


class AuditEntry(BaseModel):
    """A single audit log entry."""

    timestamp: datetime
    agent_name: str
    action: str
    details: dict = {}


class TransparencyLog(BaseModel):
    """Log of what an agent checked during its run."""

    entries: list[str] = []


class ImpactSummary(BaseModel):
    """Summarizes the impact of an event or action."""

    cost_delta: float = 0.0
    schedule_delta_days: int = 0
    risk_change: str = ""
    description: str = ""


class AgentEvent(BaseModel):
    """An event published by an agent via pub/sub."""

    event_id: str
    source_agent: str
    event_type: str
    severity: Literal["info", "warning", "critical"]
    timestamp: datetime
    data: dict = {}
    confidence: float = Field(ge=0, le=1)
    data_sources: list[DataSource] = []
    transparency_log: list[str] = []
    requires_cross_agent: bool = False
    target_agent: str | None = None


class ApprovalRequest(BaseModel):
    """A request for PM approval before taking action."""

    id: str = ""
    agent_name: str
    action_type: str
    title: str
    description: str
    confidence: float = Field(ge=0, le=100)
    data_sources: list[DataSource] = []
    transparency_log: list[str] = []
    impact: ImpactSummary = ImpactSummary()
    status: Literal["pending", "approved", "rejected"] = "pending"
    pm_notes: str | None = None
