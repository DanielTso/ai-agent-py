"""Pydantic schemas for safety compliance."""

from datetime import date, datetime

from pydantic import BaseModel


class SafetyIncidentRecord(BaseModel):
    """Safety incident record."""

    id: str
    incident_date: date
    osha_classification: str  # recordable/first_aid/near_miss/fatality
    severity: str  # minor/serious/critical/fatal
    location: str
    description: str
    recordable: bool
    lost_time_days: int
    root_cause: str | None = None


class OSHA300Record(BaseModel):
    """OSHA 300 log entry."""

    case_number: str
    employee_name: str
    job_title: str
    date_of_injury: date
    description: str
    classification: str
    days_away: int
    days_restricted: int
    death: bool


class ExposureMonitoringRecord(BaseModel):
    """Occupational exposure monitoring record."""

    id: str
    substance: str
    measured_level: float
    unit: str
    osha_pel: float
    niosh_rel: float | None = None
    action_level: float | None = None
    location: str
    worker_id: str | None = None
    compliant: bool


class ContractorSafetyProfileData(BaseModel):
    """Contractor safety profile for prequalification."""

    contractor: str
    osha_citations: list[dict]
    msha_violations: list[dict]
    emr: float | None = None
    trir: float | None = None
    dart: float | None = None
    risk_level: str  # low/medium/high/critical


class JHAEntry(BaseModel):
    """Job Hazard Analysis entry."""

    activity: str
    hazards: list[str]
    controls: list[str]
    hierarchy_of_controls: list[str]
    ppe_required: list[str]
    competent_person_required: bool


class InspectionReadinessScore(BaseModel):
    """OSHA inspection readiness score."""

    score: float
    max_score: float
    percentage: float
    categories: dict[str, float]
    deficiencies: list[str]
    recommendations: list[str]


class TrainingRecordData(BaseModel):
    """Worker training record."""

    worker_id: str
    worker_name: str
    training_type: str  # OSHA10/OSHA30/MSHA_Part46/MSHA_Part48/competent_person/first_aid/hazwoper
    completion_date: date | None = None
    expiry: date | None = None
    status: str  # valid/expiring/expired


class SafetyMetricsData(BaseModel):
    """Safety metrics for a reporting period."""

    period: str
    trir: float
    dart: float
    emr: float
    near_miss_count: int
    leading_indicators: dict
    lagging_indicators: dict


class SafetyReport(BaseModel):
    """Full safety compliance report."""

    project_id: str
    metrics: SafetyMetricsData
    incidents: list[SafetyIncidentRecord]
    osha_300: list[OSHA300Record]
    readiness: InspectionReadinessScore
    generated_at: datetime


# --- NFPA / NEC schemas ---


class NfpaCheckResult(BaseModel):
    """Single NFPA/NEC compliance check result."""

    status: str  # compliant/warning/critical
    findings: list[str]
    standard: str
    recommendations: list[str] = []


class FireProtectionReport(BaseModel):
    """NFPA fire protection compliance report."""

    project_id: str
    fire_barriers: NfpaCheckResult
    fire_dampers: NfpaCheckResult
    firestop_systems: NfpaCheckResult


class NECArticleCheck(BaseModel):
    """NEC (NFPA 70) article compliance check."""

    status: str  # compliant/warning/critical
    findings: list[str]
    standard: str
    nec_articles: list[str]
    recommendations: list[str] = []


class NECComplianceReport(BaseModel):
    """NEC compliance report across articles."""

    project_id: str
    article_checked: str
    conductor_sizing: NECArticleCheck
    overcurrent_protection: NECArticleCheck
    grounding: NECArticleCheck
    emergency_systems: NECArticleCheck


class OccupantLoadCheck(BaseModel):
    """NFPA 101 occupant load calculation."""

    floor: str
    calculated_load: int
    design_capacity: int
    compliant: bool
    standard: str


class ExitCapacityCheck(BaseModel):
    """NFPA 101 exit capacity check."""

    required_exits: int
    provided_exits: int
    exit_width_total_in: int
    required_width_in: int
    compliant: bool
    standard: str


class TravelDistanceCheck(BaseModel):
    """NFPA 101 travel distance check."""

    status: str
    max_travel_ft: int
    allowed_ft: int
    location: str
    compliant: bool
    standard: str
    recommendations: list[str] = []


class LifeSafetyReport(BaseModel):
    """NFPA 101 life safety compliance report."""

    project_id: str
    occupant_load: OccupantLoadCheck
    exit_capacity: ExitCapacityCheck
    travel_distance: TravelDistanceCheck


class SprinklerCoverage(BaseModel):
    """NFPA 13 sprinkler coverage check."""

    status: str
    system_type: str
    design_standard: str
    areas_inspected: int
    deficiencies: list[str]
    standard: str


class WaterSupply(BaseModel):
    """NFPA 13 water supply adequacy check."""

    status: str
    static_psi: int
    residual_psi: int
    flow_gpm: int
    required_gpm: int
    standard: str


class FireAlarmCheck(BaseModel):
    """NFPA 72 fire alarm system check."""

    status: str
    panel_type: str
    zones_programmed: int
    zones_verified: int
    deficiencies: list[str]
    standard: str
    recommendations: list[str] = []


class SprinklerAlarmReport(BaseModel):
    """NFPA 13/72 sprinkler and alarm report."""

    project_id: str
    sprinkler_coverage: SprinklerCoverage
    water_supply: WaterSupply
    fire_alarm: FireAlarmCheck


class EgressCheck(BaseModel):
    """NFPA 101 egress compliance report."""

    project_id: str
    corridor_width: dict
    door_swing: NfpaCheckResult
    exit_access: dict
    exit_discharge: dict
