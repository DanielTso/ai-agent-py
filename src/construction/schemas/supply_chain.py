"""Pydantic models for supply chain monitoring."""

from datetime import date, datetime

from pydantic import BaseModel, Field

from construction.schemas.common import DataSource


class VendorStatus(BaseModel):
    """Current status of a vendor."""

    id: str
    name: str
    material: str
    lead_time_days: int
    current_status: str  # on_track/delayed/at_risk/critical
    port_of_origin: str | None = None
    last_updated: datetime


class ShipmentMilestone(BaseModel):
    """A milestone in a shipment's journey."""

    description: str
    timestamp: datetime
    location: str | None = None


class ShipmentTracking(BaseModel):
    """Tracking data for a single shipment."""

    id: str
    vendor_id: str
    tracking_id: str
    eta: date | None = None
    original_eta: date | None = None
    delay_days: int = 0
    delay_reason: str | None = None
    status: str
    milestones: list[ShipmentMilestone] = []


class AlternativeSourceOption(BaseModel):
    """A possible alternative vendor/source."""

    alt_vendor: str
    cost_delta: float
    schedule_delta_days: int
    recommended: bool = False
    notes: str | None = None
    confidence: float = Field(ge=0, le=1)


class SupplyChainAlert(BaseModel):
    """An alert about a supply chain issue."""

    vendor_id: str
    shipment_id: str | None = None
    alert_type: str
    severity: str
    description: str
    alternatives: list[AlternativeSourceOption] = []
    data_sources: list[DataSource] = []


class ExpediteTemplate(BaseModel):
    """Template for expediting a delayed material."""

    vendor: str
    material: str
    current_eta: date
    options: list[AlternativeSourceOption] = []
