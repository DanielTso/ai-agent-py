// ---------------------------------------------------------------------------
// Common
// ---------------------------------------------------------------------------

export interface DataSource {
  source_type: string;
  source_name: string;
  retrieved_at: string;
  confidence: number;
}

export interface ImpactSummary {
  cost_delta: number;
  schedule_delta_days: number;
  risk_change: string;
  description: string;
}

export interface ApprovalRequest {
  id: string;
  agent_name: string;
  action_type: string;
  title: string;
  description: string;
  confidence: number;
  data_sources: DataSource[];
  transparency_log: string[];
  impact: ImpactSummary;
  status: "pending" | "approved" | "rejected";
  pm_notes: string | null;
}

export interface AgentStatus {
  name: string;
  status: "idle" | "running" | "error";
  last_run: string;
  runs_today: number;
  avg_duration_seconds: number;
  errors_today: number;
}

// ---------------------------------------------------------------------------
// Risk
// ---------------------------------------------------------------------------

export interface RiskScore {
  probability: number;
  impact_dollars: number;
  impact_days: number;
  safety_critical: boolean;
  composite_score: number;
}

export interface RiskEvent {
  id: string;
  project_id: string;
  category: string;
  description: string;
  risk_score: RiskScore;
  confidence: number;
  data_sources: DataSource[];
  transparency_log: string[];
  status: string;
  created_at: string;
  updated_at: string | null;
}

export interface RiskHeatMapCell {
  probability_range: string;
  impact_range: string;
  count: number;
  risk_ids: string[];
}

// ---------------------------------------------------------------------------
// Schedule
// ---------------------------------------------------------------------------

export interface Activity {
  id: string;
  external_id: string;
  name: string;
  start_date: string | null;
  end_date: string | null;
  total_float: number;
  is_critical: boolean;
  tier_critical: boolean;
  predecessors: string[];
  successors: string[];
}

export interface CriticalPath {
  activities: Activity[];
  total_duration_days: number;
  float_summary: Record<string, number>;
}

export interface ScheduleDelta {
  baseline_end: string;
  projected_end: string;
  delta_days: number;
  float_consumed: Record<string, number>;
  affected_activities: string[];
  description: string;
}

export interface FloatReport {
  activity_id: string;
  activity_name: string;
  total_float: number;
  free_float: number;
  status: "healthy" | "warning" | "critical";
}

export interface MonteCarloResult {
  iterations: number;
  p50_completion: string;
  p80_completion: string;
  p95_completion: string;
  confidence: number;
  float_consumed: Record<string, number>;
  histogram: Array<{ month: string; probability: number }>;
  run_at: string;
}

// ---------------------------------------------------------------------------
// Compliance
// ---------------------------------------------------------------------------

export interface ComplianceCheck {
  id: string;
  project_id: string;
  check_type: string;
  bim_element_id: string | null;
  measured_value: string | null;
  required_value: string | null;
  deviation: number | null;
  severity: "info" | "minor" | "major" | "critical";
  status: "open" | "in_progress" | "resolved" | "accepted";
  location: string | null;
  description: string | null;
  created_at: string;
}

export interface DeviationTicket {
  id: string;
  compliance_check_id: string;
  title: string;
  description: string;
  severity: string;
  bim_overlay_url: string | null;
  assigned_to: string | null;
  due_date: string | null;
  status: string;
}

// ---------------------------------------------------------------------------
// Supply Chain
// ---------------------------------------------------------------------------

export interface VendorStatus {
  id: string;
  name: string;
  material: string;
  lead_time_days: number;
  current_status: "on_track" | "delayed" | "at_risk" | "critical";
  port_of_origin: string | null;
  last_updated: string;
}

export interface ShipmentMilestone {
  description: string;
  timestamp: string;
  location: string | null;
}

export interface ShipmentTracking {
  id: string;
  vendor_id: string;
  tracking_id: string;
  eta: string | null;
  original_eta: string | null;
  delay_days: number;
  delay_reason: string | null;
  status: string;
  milestones: ShipmentMilestone[];
}

export interface AlternativeSourceOption {
  alt_vendor: string;
  cost_delta: number;
  schedule_delta_days: number;
  recommended: boolean;
  notes: string | null;
  confidence: number;
}

export interface SupplyChainAlert {
  vendor_id: string;
  shipment_id: string | null;
  alert_type: string;
  severity: string;
  description: string;
  alternatives: AlternativeSourceOption[];
}

// ---------------------------------------------------------------------------
// Financial
// ---------------------------------------------------------------------------

export interface BudgetStatus {
  project_id: string;
  total_budget: number;
  spent_to_date: number;
  committed: number;
  forecast_at_completion: number;
  contingency_remaining: number;
  variance_pct: number;
}

export interface EarnedValue {
  snapshot_date: string;
  bcws: number;
  bcwp: number;
  acwp: number;
  cpi: number;
  spi: number;
  eac: number;
  etc: number;
  vac: number;
  tcpi: number;
}

export interface CashFlow {
  period: string;
  planned_draw: number;
  actual_draw: number;
  cumulative_planned: number;
  cumulative_actual: number;
}

export interface ChangeOrder {
  id: string;
  co_number: string;
  description: string;
  cost_impact: number;
  schedule_impact_days: number;
  status: "pending" | "approved" | "rejected" | "executed";
  submitted_date: string | null;
  approved_date: string | null;
}

// ---------------------------------------------------------------------------
// Workforce
// ---------------------------------------------------------------------------

export interface CrewStatus {
  trade: string;
  headcount: number;
  planned_production: number;
  actual_production: number;
  productivity_pct: number;
  location: string | null;
  overtime_hours: number;
}

export interface ProductivityMetric {
  trade: string;
  period: string;
  planned_units: number;
  actual_units: number;
  productivity_index: number;
  trend: "improving" | "stable" | "declining";
}

export interface CertificationRecord {
  worker_id: string;
  worker_name: string;
  cert_type: string;
  issue_date: string | null;
  expiry_date: string | null;
  status: "valid" | "expiring_soon" | "expired";
}

// ---------------------------------------------------------------------------
// Orchestrator / Daily Brief
// ---------------------------------------------------------------------------

export interface ThreatSummary {
  rank: number;
  title: string;
  agent_source: string;
  impact: string;
  confidence: number;
  action_required: string;
}

export interface QualityGap {
  rank: number;
  title: string;
  agent_source: string;
  severity: string;
  location: string;
}

export interface AccelerationOpportunity {
  title: string;
  agent_source: string;
  potential_savings_days: number;
  cost: number;
  description: string;
}

export interface DailyBrief {
  brief_date: string;
  generated_at: string;
  top_threats: ThreatSummary[];
  quality_gaps: QualityGap[];
  acceleration: AccelerationOpportunity | null;
  full_text: string;
}

// ---------------------------------------------------------------------------
// Safety
// ---------------------------------------------------------------------------

export interface SafetyMetrics {
  trir: number;
  dart: number;
  emr: number;
  days_since_recordable: number;
  near_misses_ytd: number;
  first_aid_ytd: number;
  recordables_ytd: number;
  man_hours_ytd: number;
}

export interface OSHA300Record {
  case_number: string;
  employee: string;
  date_of_injury: string;
  description: string;
  classification: string;
  days_away: number;
  days_restricted: number;
  body_part: string;
}

export interface InspectionReadiness {
  overall_score: number;
  categories: Array<{
    name: string;
    score: number;
    status: string;
  }>;
}

export interface ContractorSafetyProfile {
  contractor: string;
  emr: number;
  trir: number;
  prequalified: boolean;
  incidents_ytd: number;
  training_compliance_pct: number;
}

// ---------------------------------------------------------------------------
// Commissioning
// ---------------------------------------------------------------------------

export interface ISTSequence {
  id: string;
  system: string;
  status: string;
  progress_pct: number;
  tests_passed: number;
  tests_total: number;
  next_test: string;
}

export interface PunchItem {
  id: string;
  description: string;
  system: string;
  location: string;
  severity: string;
  assigned_to: string | null;
  status: string;
}

export interface TurnoverPackage {
  id: string;
  system: string;
  documents_complete: number;
  documents_required: number;
  progress_pct: number;
  status: string;
  missing: string[];
}

// ---------------------------------------------------------------------------
// Environmental
// ---------------------------------------------------------------------------

export interface PermitStatus {
  id: string;
  permit_type: string;
  description: string;
  status: string;
  expiry_date: string;
  inspector: string;
  last_inspection: string;
}

export interface LEEDCredit {
  name: string;
  earned: number;
  possible: number;
}

export interface LEEDTracking {
  target_level: string;
  current_points: number;
  target_points: number;
  categories: LEEDCredit[];
}

// ---------------------------------------------------------------------------
// Claims
// ---------------------------------------------------------------------------

export interface ClaimEvent {
  id: string;
  title: string;
  type: string;
  amount: number;
  filed_date: string;
  status: string;
  milestones: Array<{ date: string; event: string }>;
}

export interface NoticeRecord {
  id: string;
  notice_type: string;
  from_party: string;
  to_party: string;
  subject: string;
  sent_date: string;
  response_due: string;
  status: string;
}

export interface DelayAnalysis {
  method: string;
  baseline_completion: string;
  projected_completion: string;
  total_delay_days: number;
  excusable_days: number;
  non_excusable_days: number;
  compensable_days: number;
  delay_events: Array<{
    id: string;
    description: string;
    delay_days: number;
    excusable: boolean;
    compensable: boolean;
  }>;
}

// ---------------------------------------------------------------------------
// Site Logistics
// ---------------------------------------------------------------------------

export interface CraneScheduleEntry {
  id: string;
  crane_id: string;
  date: string;
  time_slots: Array<{
    start: string;
    end: string;
    trade: string;
    description: string;
  }>;
}

export interface StagingPlan {
  id: string;
  zone: string;
  capacity_pct: number;
  current_materials: string[];
  reserved_until: string;
  status: string;
}

export interface SiteHeadcount {
  date: string;
  total: number;
  by_trade: Array<{ trade: string; count: number }>;
}
