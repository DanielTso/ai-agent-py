"""Repository classes for Construction PM database access."""

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from construction.db.models import (
    ApprovalRequest,
    ComplianceCheck,
    DailyBrief,
    Document,
    RiskEvent,
    SafetyIncident,
    SafetyInspection,
    SafetyMetric,
    ScheduleActivity,
    Shipment,
    Vendor,
)


class BaseRepository:
    """Generic async CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model_cls, **kwargs):
        """Create and persist a new instance."""
        instance = model_cls(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_by_id(self, model_cls, id: uuid.UUID):
        """Fetch a single record by primary key."""
        return await self.session.get(model_cls, id)

    async def list_all(self, model_cls, **filters):
        """List records, optionally filtered by column values."""
        stmt = select(model_cls)
        for key, value in filters.items():
            stmt = stmt.where(getattr(model_cls, key) == value)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, instance, **kwargs):
        """Update fields on an existing instance."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, instance):
        """Delete an instance."""
        await self.session.delete(instance)
        await self.session.flush()


class RiskRepository(BaseRepository):
    """Queries specific to risk events."""

    async def list_active_risks(self, project_id: uuid.UUID):
        """Return all active risks for a project."""
        stmt = (
            select(RiskEvent)
            .where(RiskEvent.project_id == project_id)
            .where(RiskEvent.status == "active")
            .order_by(RiskEvent.probability.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_safety_critical(self, project_id: uuid.UUID):
        """Return safety-critical risk events."""
        stmt = (
            select(RiskEvent)
            .where(RiskEvent.project_id == project_id)
            .where(RiskEvent.safety_critical.is_(True))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_high_impact(self, project_id: uuid.UUID, threshold: float):
        """Return risks exceeding a dollar impact threshold."""
        stmt = (
            select(RiskEvent)
            .where(RiskEvent.project_id == project_id)
            .where(RiskEvent.impact_dollars >= threshold)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class DocumentRepository(BaseRepository):
    """Queries specific to documents and contradictions."""

    async def list_by_type(self, project_id: uuid.UUID, doc_type: str):
        """Return documents of a given type."""
        stmt = (
            select(Document)
            .where(Document.project_id == project_id)
            .where(Document.doc_type == doc_type)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_by_title(self, project_id: uuid.UUID, query: str):
        """Simple title search (case-insensitive LIKE)."""
        stmt = (
            select(Document)
            .where(Document.project_id == project_id)
            .where(Document.title.ilike(f"%{query}%"))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ScheduleRepository(BaseRepository):
    """Queries specific to schedule activities and simulations."""

    async def list_critical_path(self, project_id: uuid.UUID):
        """Return activities on the critical path."""
        stmt = (
            select(ScheduleActivity)
            .where(ScheduleActivity.project_id == project_id)
            .where(ScheduleActivity.is_critical.is_(True))
            .order_by(ScheduleActivity.start_date)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_low_float(self, project_id: uuid.UUID, threshold: float):
        """Return activities with total float below threshold."""
        stmt = (
            select(ScheduleActivity)
            .where(ScheduleActivity.project_id == project_id)
            .where(ScheduleActivity.total_float <= threshold)
            .order_by(ScheduleActivity.total_float)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ComplianceRepository(BaseRepository):
    """Queries specific to compliance checks."""

    async def list_open_issues(self, project_id: uuid.UUID):
        """Return open compliance issues."""
        stmt = (
            select(ComplianceCheck)
            .where(ComplianceCheck.project_id == project_id)
            .where(ComplianceCheck.status == "open")
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_severity(self, project_id: uuid.UUID, severity: str):
        """Return compliance checks of a given severity."""
        stmt = (
            select(ComplianceCheck)
            .where(ComplianceCheck.project_id == project_id)
            .where(ComplianceCheck.severity == severity)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class VendorRepository(BaseRepository):
    """Queries specific to vendors and shipments."""

    async def list_delayed_shipments(self, project_id: uuid.UUID):
        """Return shipments with delays."""
        stmt = (
            select(Shipment)
            .where(Shipment.project_id == project_id)
            .where(Shipment.delay_days > 0)
            .order_by(Shipment.delay_days.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_vendors_by_material(self, project_id: uuid.UUID, material: str):
        """Return vendors supplying a given material."""
        stmt = (
            select(Vendor).where(Vendor.project_id == project_id).where(Vendor.material == material)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ApprovalRepository(BaseRepository):
    """Queries specific to approval requests."""

    async def list_pending(self, project_id: uuid.UUID):
        """Return pending approval requests."""
        stmt = (
            select(ApprovalRequest)
            .where(ApprovalRequest.project_id == project_id)
            .where(ApprovalRequest.status == "pending")
            .order_by(ApprovalRequest.created_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class DailyBriefRepository(BaseRepository):
    """Queries specific to daily briefs."""

    async def get_latest(self, project_id: uuid.UUID):
        """Return the most recent daily brief."""
        stmt = (
            select(DailyBrief)
            .where(DailyBrief.project_id == project_id)
            .order_by(DailyBrief.brief_date.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_date(self, project_id: uuid.UUID, brief_date: date):
        """Return the brief for a specific date."""
        stmt = (
            select(DailyBrief)
            .where(DailyBrief.project_id == project_id)
            .where(DailyBrief.brief_date == brief_date)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SafetyRepository(BaseRepository):
    """Queries specific to safety records."""

    async def list_incidents(self, project_id: uuid.UUID):
        """Return all safety incidents for a project."""
        stmt = (
            select(SafetyIncident)
            .where(SafetyIncident.project_id == project_id)
            .order_by(SafetyIncident.incident_date.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_open_inspections(self, project_id: uuid.UUID):
        """Return inspections with open abatement status."""
        stmt = (
            select(SafetyInspection)
            .where(SafetyInspection.project_id == project_id)
            .where(SafetyInspection.abatement_status == "open")
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_latest_metrics(self, project_id: uuid.UUID):
        """Return the most recent safety metrics."""
        stmt = (
            select(SafetyMetric)
            .where(SafetyMetric.project_id == project_id)
            .order_by(SafetyMetric.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
