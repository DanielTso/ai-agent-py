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


# --- ICC Building Codes schemas ---


class ICCCheckResult(BaseModel):
    """Single ICC code compliance check result."""

    status: str  # compliant/warning/critical
    findings: list[str]
    code_section: str
    recommendations: list[str] = []


class OccupancyClassification(BaseModel):
    """IBC occupancy classification for a building zone."""

    zone: str
    occupancy_group: str  # B/S-1/F-1/I-2/A-1 etc.
    occupancy_description: str
    code_section: str
    construction_type: str  # Type I-A, II-B, etc.
    height_limit_ft: int | str  # "unlimited" or numeric
    area_limit_sqft: int | str
    height_area_compliant: bool


class IBCReport(BaseModel):
    """IBC (International Building Code) compliance report."""

    project_id: str
    occupancy_classification: list[OccupancyClassification]
    construction_type: str
    height_area_compliance: bool
    structural_requirements: dict
    accessibility_checks: dict
    means_of_egress: dict
    fire_resistance: dict
    code_sections_referenced: list[str]


class IFCReport(BaseModel):
    """IFC (International Fire Code) compliance report."""

    project_id: str
    fire_access: ICCCheckResult
    fire_protection_systems: ICCCheckResult
    hazmat_storage: ICCCheckResult
    construction_fire_safety: ICCCheckResult


class IMCReport(BaseModel):
    """IMC (International Mechanical Code) compliance report."""

    project_id: str
    ventilation_rates: ICCCheckResult
    equipment_compliance: ICCCheckResult
    ductwork_standards: ICCCheckResult
    energy_recovery: ICCCheckResult


class IPCReport(BaseModel):
    """IPC (International Plumbing Code) compliance report."""

    project_id: str
    fixture_compliance: ICCCheckResult
    drainage_system: ICCCheckResult
    water_supply: ICCCheckResult
    backflow_prevention: ICCCheckResult


class IECCReport(BaseModel):
    """IECC (International Energy Conservation Code) report."""

    project_id: str
    envelope_compliance: ICCCheckResult
    lighting_compliance: ICCCheckResult
    hvac_efficiency: ICCCheckResult
    commissioning_requirements: ICCCheckResult


# --- Uptime Institute Tier certification schemas ---


class TierRequirements(BaseModel):
    """Uptime Institute Tier level requirements."""

    tier_level: str  # I/II/III/IV
    name: str
    redundancy: str  # N/N+1/2N/2N+1/2(N+1)
    uptime: str
    annual_downtime_hours: float
    power: dict[str, str]
    cooling: dict[str, str]
    network: dict[str, str]
    fire_suppression: dict[str, str]


class RedundancyComponent(BaseModel):
    """Single infrastructure component redundancy status."""

    component: str
    required: str
    installed: str
    status: str  # compliant/non_compliant/warning
    issue: str | None = None


class RedundancyDeficiency(BaseModel):
    """A redundancy deficiency found during check."""

    id: str
    description: str
    severity: str  # warning/non_compliant
    recommendation: str


class RedundancySystemCheck(BaseModel):
    """Redundancy check result for one infrastructure system."""

    system: str  # power/cooling/network/fire_suppression
    tier_level: str
    components: list[RedundancyComponent]
    findings: list[str]
    deficiencies: list[RedundancyDeficiency]


class RedundancyReport(BaseModel):
    """Full redundancy check report across systems."""

    project_id: str
    tier_level: str
    overall_status: str  # compliant/warning/non_compliant
    systems: dict[str, RedundancySystemCheck]


class MaintenancePathComponent(BaseModel):
    """Concurrent maintainability data for a component."""

    can_maintain_without_load_transfer: bool | None = None
    can_maintain_without_impact: bool | None = None
    maintenance_path: str
    isolation_points: list[str]
    bypass_capability: bool


class ConcurrentMaintainabilitySystem(BaseModel):
    """Concurrent maintainability check for one system."""

    system: str
    concurrently_maintainable: bool
    components: dict[str, MaintenancePathComponent]
    findings: list[str]


class ConcurrentMaintainabilityReport(BaseModel):
    """Tier III concurrent maintainability report."""

    project_id: str
    tier_iii_concurrent_maintainability: bool
    systems: dict[str, ConcurrentMaintainabilitySystem]


class FaultAnalysisComponent(BaseModel):
    """Single-point-of-failure analysis for a component."""

    dual_active_paths: bool | None = None
    automatic_fault_isolation: bool | None = None
    no_single_point_of_failure: bool | None = None
    compartmentalized: bool | None = None
    auto_failover: bool | None = None
    transfer_time_ms: int | None = None
    max_allowed_ms: int | None = None
    auto_start_time_seconds: int | None = None
    fire_rated_separation: bool | None = None
    status: str  # pass/fail
    issue: str | None = None


class FaultToleranceSystem(BaseModel):
    """Fault tolerance check for one system."""

    system: str
    fault_tolerant: bool
    single_point_of_failure_analysis: dict[str, FaultAnalysisComponent]
    automatic_response: dict[str, str]
    findings: list[str]


class FaultToleranceReport(BaseModel):
    """Tier IV fault tolerance report."""

    project_id: str
    tier_iv_fault_tolerant: bool
    systems: dict[str, FaultToleranceSystem]


class CertificationPhase(BaseModel):
    """Status of one certification phase."""

    status: str  # approved/in_progress/not_started
    score: int | None = None
    date: str | None = None
    expected_completion: str | None = None
    prerequisite: str | None = None
    findings: list[str]


class TierCertificationStatus(BaseModel):
    """Overall Uptime Institute Tier certification status."""

    project_id: str
    target_tier: str
    design_certification: CertificationPhase
    construction_certification: CertificationPhase
    operational_sustainability: CertificationPhase
