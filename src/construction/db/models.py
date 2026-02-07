"""SQLAlchemy ORM models for the Construction PM ecosystem."""

import uuid
from datetime import date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base for all Construction PM models."""


def _uuid4():
    return uuid.uuid4()


# ---------------------------------------------------------------------------
# Mixin for common columns
# ---------------------------------------------------------------------------
class TimestampMixin:
    """Provides id, created_at, updated_at to all models."""

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


# ===========================================================================
# Core tables
# ===========================================================================


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, nullable=False)
    tier_level: Mapped[str] = mapped_column(String, nullable=False)
    site_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    site_lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    target_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    contract_value: Mapped[float] = mapped_column(Float, nullable=False)

    # relationships
    risk_events: Mapped[list["RiskEvent"]] = relationship(back_populates="project")
    documents: Mapped[list["Document"]] = relationship(back_populates="project")
    schedule_activities: Mapped[list["ScheduleActivity"]] = relationship(back_populates="project")
    compliance_checks: Mapped[list["ComplianceCheck"]] = relationship(back_populates="project")
    vendors: Mapped[list["Vendor"]] = relationship(back_populates="project")
    approval_requests: Mapped[list["ApprovalRequest"]] = relationship(back_populates="project")
    daily_briefs: Mapped[list["DailyBrief"]] = relationship(back_populates="project")


class RiskEvent(TimestampMixin, Base):
    __tablename__ = "risk_events"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    probability: Mapped[float] = mapped_column(Float, nullable=False)
    impact_dollars: Mapped[float] = mapped_column(Float, nullable=False)
    impact_days: Mapped[float] = mapped_column(Float, nullable=False)
    safety_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    data_sources: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")
    transparency_log: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="risk_events")


class Document(TimestampMixin, Base):
    __tablename__ = "documents"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    doc_type: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata_", JSON, nullable=True)
    version: Mapped[str | None] = mapped_column(String, nullable=True)
    author: Mapped[str | None] = mapped_column(String, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="documents")
    contradictions_as_a: Mapped[list["DocumentContradiction"]] = relationship(
        foreign_keys="DocumentContradiction.doc_a_id", back_populates="doc_a"
    )
    contradictions_as_b: Mapped[list["DocumentContradiction"]] = relationship(
        foreign_keys="DocumentContradiction.doc_b_id", back_populates="doc_b"
    )


class DocumentContradiction(TimestampMixin, Base):
    __tablename__ = "document_contradictions"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    doc_a_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
    doc_b_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="open")

    doc_a: Mapped["Document"] = relationship(
        foreign_keys=[doc_a_id], back_populates="contradictions_as_a"
    )
    doc_b: Mapped["Document"] = relationship(
        foreign_keys=[doc_b_id], back_populates="contradictions_as_b"
    )


class ScheduleActivity(TimestampMixin, Base):
    __tablename__ = "schedule_activities"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    external_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_float: Mapped[float] = mapped_column(Float, default=0)
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    tier_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    predecessors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    successors: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="schedule_activities")
    simulations: Mapped[list["ScheduleSimulation"]] = relationship(back_populates="activity")


class ScheduleSimulation(TimestampMixin, Base):
    __tablename__ = "schedule_simulations"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    activity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("schedule_activities.id"), nullable=True
    )
    iterations: Mapped[int] = mapped_column(Integer, nullable=False)
    p50_completion: Mapped[date | None] = mapped_column(Date, nullable=True)
    p80_completion: Mapped[date | None] = mapped_column(Date, nullable=True)
    p95_completion: Mapped[date | None] = mapped_column(Date, nullable=True)
    float_consumed: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    run_params: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    activity: Mapped["ScheduleActivity | None"] = relationship(back_populates="simulations")


class ComplianceCheck(TimestampMixin, Base):
    __tablename__ = "compliance_checks"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    check_type: Mapped[str] = mapped_column(String, nullable=False)
    bim_element_id: Mapped[str | None] = mapped_column(String, nullable=True)
    measured_value: Mapped[str | None] = mapped_column(String, nullable=True)
    required_value: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="open")
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="compliance_checks")


class Vendor(TimestampMixin, Base):
    __tablename__ = "vendors"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    material: Mapped[str] = mapped_column(String, nullable=False)
    lead_time_days: Mapped[int] = mapped_column(Integer, nullable=False)
    current_status: Mapped[str] = mapped_column(String, nullable=False)
    port_of_origin: Mapped[str | None] = mapped_column(String, nullable=True)
    contact_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="vendors")
    shipments: Mapped[list["Shipment"]] = relationship(back_populates="vendor")
    alternative_sources: Mapped[list["AlternativeSource"]] = relationship(
        back_populates="original_vendor"
    )


class Shipment(TimestampMixin, Base):
    __tablename__ = "shipments"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    vendor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vendors.id"))
    tracking_id: Mapped[str] = mapped_column(String, nullable=False)
    eta: Mapped[date | None] = mapped_column(Date, nullable=True)
    original_eta: Mapped[date | None] = mapped_column(Date, nullable=True)
    delay_days: Mapped[int] = mapped_column(Integer, default=0)
    delay_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)

    vendor: Mapped["Vendor"] = relationship(back_populates="shipments")


class AlternativeSource(TimestampMixin, Base):
    __tablename__ = "alternative_sources"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    original_vendor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vendors.id"))
    shipment_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("shipments.id"), nullable=True)
    alt_vendor: Mapped[str] = mapped_column(String, nullable=False)
    cost_delta: Mapped[float] = mapped_column(Float, nullable=False)
    schedule_delta_days: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    original_vendor: Mapped["Vendor"] = relationship(back_populates="alternative_sources")


class ApprovalRequest(TimestampMixin, Base):
    __tablename__ = "approval_requests"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    action_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    data_sources: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    transparency_log: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    impact_cost_delta: Mapped[float | None] = mapped_column(Float, nullable=True)
    impact_schedule_delta_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    impact_risk_change: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    pm_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="approval_requests")


class DailyBrief(TimestampMixin, Base):
    __tablename__ = "daily_briefs"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    brief_date: Mapped[date] = mapped_column(Date, nullable=False)
    top_threats: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    quality_gaps: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    acceleration: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    full_text: Mapped[str] = mapped_column(Text, nullable=False)

    project: Mapped["Project"] = relationship(back_populates="daily_briefs")


class AgentRun(TimestampMixin, Base):
    __tablename__ = "agent_runs"

    project_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    trigger: Mapped[str] = mapped_column(String, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default="running")
    output_summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_log"

    project_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)


# ===========================================================================
# Extended tables (Phase 3)
# ===========================================================================


class BudgetItem(TimestampMixin, Base):
    __tablename__ = "budget_items"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    planned_cost: Mapped[float] = mapped_column(Float, nullable=False)
    actual_cost: Mapped[float] = mapped_column(Float, default=0)
    forecast_cost: Mapped[float] = mapped_column(Float, default=0)
    variance: Mapped[float] = mapped_column(Float, default=0)


class ChangeOrder(TimestampMixin, Base):
    __tablename__ = "change_orders"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    co_number: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    cost_impact: Mapped[float] = mapped_column(Float, nullable=False)
    schedule_impact_days: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")


class EarnedValueSnapshot(TimestampMixin, Base):
    __tablename__ = "earned_value_snapshots"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    bcws: Mapped[float] = mapped_column(Float, nullable=False)
    bcwp: Mapped[float] = mapped_column(Float, nullable=False)
    acwp: Mapped[float] = mapped_column(Float, nullable=False)
    cpi: Mapped[float] = mapped_column(Float, nullable=False)
    spi: Mapped[float] = mapped_column(Float, nullable=False)
    eac: Mapped[float] = mapped_column(Float, nullable=False)
    etc_: Mapped[float] = mapped_column("etc_", Float, nullable=False)


class CrewAssignment(TimestampMixin, Base):
    __tablename__ = "crew_assignments"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    trade: Mapped[str] = mapped_column(String, nullable=False)
    headcount: Mapped[int] = mapped_column(Integer, nullable=False)
    planned_production: Mapped[float] = mapped_column(Float, nullable=False)
    actual_production: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)


class Certification(TimestampMixin, Base):
    __tablename__ = "certifications"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    worker_id: Mapped[str] = mapped_column(String, nullable=False)
    worker_name: Mapped[str] = mapped_column(String, nullable=False)
    cert_type: Mapped[str] = mapped_column(String, nullable=False)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class CommunicationsLog(TimestampMixin, Base):
    __tablename__ = "communications_log"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    comm_type: Mapped[str] = mapped_column(String, nullable=False)
    recipient: Mapped[str | None] = mapped_column(String, nullable=True)
    subject: Mapped[str | None] = mapped_column(String, nullable=True)
    draft_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, default="draft")


# ===========================================================================
# Advanced tables (Phase 4)
# ===========================================================================


class CommissioningTest(TimestampMixin, Base):
    __tablename__ = "commissioning_tests"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    test_id: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    prerequisites: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    witness_required: Mapped[bool] = mapped_column(Boolean, default=False)


class PunchItem(TimestampMixin, Base):
    __tablename__ = "punch_items"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    location: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    commissioning_impact: Mapped[bool] = mapped_column(Boolean, default=False)
    assigned_to: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="open")


class TurnoverPackage(TimestampMixin, Base):
    __tablename__ = "turnover_packages"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    package_name: Mapped[str] = mapped_column(String, nullable=False)
    required_docs: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    completion_pct: Mapped[float] = mapped_column(Float, default=0)


class EnvironmentalPermit(TimestampMixin, Base):
    __tablename__ = "environmental_permits"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    permit_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    expiry: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_inspection: Mapped[date | None] = mapped_column(Date, nullable=True)


class LEEDCredit(TimestampMixin, Base):
    __tablename__ = "leed_credits"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    credit_id: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    points: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")


class ClaimEvent(TimestampMixin, Base):
    __tablename__ = "claim_events"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    causation_chain: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    notice_required: Mapped[bool] = mapped_column(Boolean, default=False)
    notice_deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    notice_sent: Mapped[bool] = mapped_column(Boolean, default=False)


class DelayAnalysis(TimestampMixin, Base):
    __tablename__ = "delay_analyses"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    analysis_type: Mapped[str] = mapped_column(String, nullable=False)
    affected_activities: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    responsible_party: Mapped[str | None] = mapped_column(String, nullable=True)
    impact_days: Mapped[float] = mapped_column(Float, default=0)


class CraneSchedule(TimestampMixin, Base):
    __tablename__ = "crane_schedules"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    crane_id: Mapped[str] = mapped_column(String, nullable=False)
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    time_slots: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    trade: Mapped[str | None] = mapped_column(String, nullable=True)
    activity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("schedule_activities.id"), nullable=True
    )


class StagingZone(TimestampMixin, Base):
    __tablename__ = "staging_zones"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    zone_id: Mapped[str] = mapped_column(String, nullable=False)
    capacity_sqft: Mapped[float] = mapped_column(Float, nullable=False)
    current_usage: Mapped[float] = mapped_column(Float, default=0)
    materials: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class SafetyIncident(TimestampMixin, Base):
    __tablename__ = "safety_incidents"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    osha_classification: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    recordable: Mapped[bool] = mapped_column(Boolean, default=False)
    lost_time_days: Mapped[int] = mapped_column(Integer, default=0)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)


class SafetyMetric(TimestampMixin, Base):
    __tablename__ = "safety_metrics"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    period: Mapped[str] = mapped_column(String, nullable=False)
    trir: Mapped[float] = mapped_column(Float, nullable=False)
    dart: Mapped[float] = mapped_column(Float, nullable=False)
    emr: Mapped[float] = mapped_column(Float, nullable=False)
    near_miss_count: Mapped[int] = mapped_column(Integer, default=0)
    leading_indicators: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class ContractorSafetyProfile(TimestampMixin, Base):
    __tablename__ = "contractor_safety_profiles"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    contractor: Mapped[str] = mapped_column(String, nullable=False)
    osha_citations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    msha_violations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    emr: Mapped[float | None] = mapped_column(Float, nullable=True)
    trir: Mapped[float | None] = mapped_column(Float, nullable=True)


class ExposureMonitoring(TimestampMixin, Base):
    __tablename__ = "exposure_monitoring"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    substance: Mapped[str] = mapped_column(String, nullable=False)
    measured_level: Mapped[float] = mapped_column(Float, nullable=False)
    osha_pel: Mapped[float] = mapped_column(Float, nullable=False)
    niosh_rel: Mapped[float | None] = mapped_column(Float, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=False)
    worker_id: Mapped[str | None] = mapped_column(String, nullable=True)


class SafetyTraining(TimestampMixin, Base):
    __tablename__ = "safety_training"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    worker_id: Mapped[str] = mapped_column(String, nullable=False)
    worker_name: Mapped[str] = mapped_column(String, nullable=False)
    training_type: Mapped[str] = mapped_column(String, nullable=False)
    completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry: Mapped[date | None] = mapped_column(Date, nullable=True)


class JHARecord(TimestampMixin, Base):
    __tablename__ = "jha_records"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    activity: Mapped[str] = mapped_column(String, nullable=False)
    hazards: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    controls: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    hierarchy_of_controls: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class SafetyInspection(TimestampMixin, Base):
    __tablename__ = "safety_inspections"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    inspection_type: Mapped[str] = mapped_column(String, nullable=False)
    findings: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    abatement_status: Mapped[str] = mapped_column(String, default="open")
    readiness_score: Mapped[float] = mapped_column(Float, default=0)


class SitePermit(TimestampMixin, Base):
    __tablename__ = "site_permits"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    permit_type: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    issued_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
