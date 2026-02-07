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


# --- EPA compliance schemas ---


class NPDESPermit(BaseModel):
    """NPDES (Clean Water Act) permit record."""

    permit_id: str
    type: str  # Construction General Permit / Individual
    status: str  # active / expired / pending
    effective_date: date | None = None
    expiration_date: date | None = None
    facility: str


class DischargeSample(BaseModel):
    """Discharge monitoring report sample result."""

    parameter: str  # pH / TSS / BOD5 / Oil & Grease
    result: float
    unit: str
    effluent_limit: float | None = None
    effluent_limit_low: float | None = None
    effluent_limit_high: float | None = None
    compliant: bool


class NPDESReport(BaseModel):
    """NPDES compliance report for a project."""

    project_id: str
    permits: list[NPDESPermit]
    discharge_monitoring: list[DischargeSample]
    exceedances: list[DischargeSample]
    compliance_status: str  # compliant / violation / pending
    last_sampling_date: date | None = None


class AmbientReading(BaseModel):
    """Ambient air quality reading."""

    parameter: str  # PM2.5 / PM10 / Fugitive Dust
    measured: float
    unit: str
    naaqs_limit: float
    compliant: bool
    source: str


class EquipmentEmission(BaseModel):
    """Construction equipment emission record."""

    equipment: str
    pollutant: str
    rate: float
    unit: str
    permit_limit: float
    compliant: bool


class AirQualityReport(BaseModel):
    """CAA air quality compliance report."""

    project_id: str
    location: str
    ambient_readings: list[AmbientReading]
    equipment_emissions: list[EquipmentEmission]
    aqi_index: int
    exceedances: list[AmbientReading]
    control_measures: list[str]
    recommended_controls: list[str]


class HazardousWasteStream(BaseModel):
    """RCRA hazardous waste stream record."""

    waste_code: str  # D001 / D007 / etc.
    description: str
    quantity_lbs: float
    storage_area: str
    accumulation_start: date | None = None
    days_in_storage: int
    max_days_allowed: int
    compliant: bool


class WasteManifest(BaseModel):
    """RCRA hazardous waste manifest."""

    manifest_id: str
    waste_code: str
    transporter: str
    tsdf: str
    ship_date: date | None = None
    received: bool


class ContainerInspection(BaseModel):
    """RCRA container inspection record."""

    area: str
    last_inspection: date | None = None
    condition: str  # good / damaged / leaking
    labels_correct: bool
    closed_properly: bool


class RCRAReport(BaseModel):
    """RCRA hazardous waste compliance report."""

    project_id: str
    generator_status: str  # VSQG / SQG / LQG
    epa_id: str
    waste_streams: list[HazardousWasteStream]
    manifests: list[WasteManifest]
    container_inspections: list[ContainerInspection]
    violations: list[str]


class BMPFinding(BaseModel):
    """Stormwater BMP inspection finding."""

    bmp: str
    status: str  # functional / damaged / needs_cleanout
    action_required: str | None = None
    priority: str | None = None  # high / medium / low


class StormwaterInspection(BaseModel):
    """Stormwater SWPPP inspection result."""

    inspection_id: str
    date: date
    inspector: str
    type: str  # routine_weekly / post_storm
    overall_status: str
    findings: list[BMPFinding]


class CorrectiveAction(BaseModel):
    """Stormwater corrective action item."""

    id: str
    finding: str
    assigned_to: str
    due_date: date | None = None
    status: str  # open / in_progress / completed


class StormwaterReport(BaseModel):
    """Construction General Permit stormwater report."""

    project_id: str
    cgp_permit: str
    swppp_current: bool
    stabilization_pct: float
    inspection_results: list[StormwaterInspection]
    corrective_actions: list[CorrectiveAction]


class PublicCommentPeriod(BaseModel):
    """NEPA public comment period status."""

    start: date | None = None
    end: date | None = None
    comments_received: int = 0
    status: str  # open / closed


class NEPAReport(BaseModel):
    """NEPA environmental review status report."""

    project_id: str
    review_type: str  # EIS / EA / Categorical Exclusion
    status: str  # in_progress / FONSI issued / ROD issued
    lead_agency: str
    filing_date: date | None = None
    decision_date: date | None = None
    findings: list[str]
    mitigation_measures: list[str]
    public_comment_period: PublicCommentPeriod
    categorical_exclusion: bool
