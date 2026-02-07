import type {
  AgentStatus,
  ApprovalRequest,
  BudgetStatus,
  CashFlow,
  ChangeOrder,
  ClaimEvent,
  ComplianceCheck,
  ContractorSafetyProfile,
  CraneScheduleEntry,
  CrewStatus,
  CertificationRecord,
  CriticalPath,
  DailyBrief,
  DelayAnalysis,
  DeviationTicket,
  EarnedValue,
  FloatReport,
  InspectionReadiness,
  LEEDTracking,
  MonteCarloResult,
  NoticeRecord,
  OSHA300Record,
  PermitStatus,
  ProductivityMetric,
  PunchItem,
  ISTSequence,
  RiskEvent,
  RiskHeatMapCell,
  SafetyMetrics,
  ShipmentTracking,
  SiteHeadcount,
  StagingPlan,
  SupplyChainAlert,
  TurnoverPackage,
  VendorStatus,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// ---------------------------------------------------------------------------
// Risks
// ---------------------------------------------------------------------------

export const risksApi = {
  list: () => fetchApi<RiskEvent[]>("/api/risks"),
  heatmap: () =>
    fetchApi<{ cells: RiskHeatMapCell[] }>("/api/risks/heatmap"),
  assess: (data: { project_id: string; categories?: string[]; timeframe_days?: number }) =>
    fetchApi("/api/risks/assess", { method: "POST", body: JSON.stringify(data) }),
};

// ---------------------------------------------------------------------------
// Schedule
// ---------------------------------------------------------------------------

export const scheduleApi = {
  criticalPath: () => fetchApi<CriticalPath>("/api/schedule/critical-path"),
  simulate: (data: { project_id: string; iterations?: number }) =>
    fetchApi<MonteCarloResult>("/api/schedule/simulate", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  floatReport: () => fetchApi<FloatReport[]>("/api/schedule/float-report"),
};

// ---------------------------------------------------------------------------
// Documents
// ---------------------------------------------------------------------------

export const documentsApi = {
  search: (query: string) =>
    fetchApi("/api/documents/search", {
      method: "POST",
      body: JSON.stringify({ query }),
    }),
  contradictions: () => fetchApi("/api/documents/contradictions"),
};

// ---------------------------------------------------------------------------
// Compliance
// ---------------------------------------------------------------------------

export const complianceApi = {
  tickets: () => fetchApi<DeviationTicket[]>("/api/compliance/tickets"),
  check: () =>
    fetchApi<{ checks: ComplianceCheck[] }>("/api/compliance/check", { method: "POST" }),
  summary: () => fetchApi("/api/compliance/summary"),
};

// ---------------------------------------------------------------------------
// Supply Chain
// ---------------------------------------------------------------------------

export const supplyChainApi = {
  vendors: () => fetchApi<VendorStatus[]>("/api/supply-chain/vendors"),
  alerts: () => fetchApi<SupplyChainAlert[]>("/api/supply-chain/alerts"),
  shipments: () => fetchApi<ShipmentTracking[]>("/api/supply-chain/shipments"),
  alternatives: () =>
    fetchApi("/api/supply-chain/alternatives", { method: "POST" }),
};

// ---------------------------------------------------------------------------
// Financial
// ---------------------------------------------------------------------------

export const financialApi = {
  evm: () => fetchApi<EarnedValue>("/api/financial/evm"),
  cashflow: () => fetchApi<CashFlow[]>("/api/financial/cashflow"),
  budget: () => fetchApi<BudgetStatus>("/api/financial/budget"),
  changeOrders: () => fetchApi<ChangeOrder[]>("/api/financial/change-orders"),
};

// ---------------------------------------------------------------------------
// Workforce
// ---------------------------------------------------------------------------

export const workforceApi = {
  crews: () => fetchApi<CrewStatus[]>("/api/workforce/crews"),
  productivity: () => fetchApi<ProductivityMetric[]>("/api/workforce/productivity"),
  certs: () => fetchApi<CertificationRecord[]>("/api/workforce/certs"),
  forecast: () => fetchApi("/api/workforce/forecast"),
};

// ---------------------------------------------------------------------------
// Briefs
// ---------------------------------------------------------------------------

export const briefsApi = {
  daily: () => fetchApi<DailyBrief>("/api/briefs/daily"),
  byDate: (date: string) => fetchApi<DailyBrief>(`/api/briefs/${date}`),
};

// ---------------------------------------------------------------------------
// Approvals
// ---------------------------------------------------------------------------

export const approvalsApi = {
  list: () => fetchApi<ApprovalRequest[]>("/api/approvals"),
  get: (id: string) => fetchApi<ApprovalRequest>(`/api/approvals/${id}`),
  approve: (id: string, notes: string) =>
    fetchApi<ApprovalRequest>(`/api/approvals/${id}/approve`, {
      method: "POST",
      body: JSON.stringify({ notes }),
    }),
  reject: (id: string, notes: string) =>
    fetchApi<ApprovalRequest>(`/api/approvals/${id}/reject`, {
      method: "POST",
      body: JSON.stringify({ notes }),
    }),
};

// ---------------------------------------------------------------------------
// Agents
// ---------------------------------------------------------------------------

export const agentsApi = {
  status: () => fetchApi<AgentStatus[]>("/api/agents/status"),
  trigger: (agentName: string) =>
    fetchApi(`/api/agents/${agentName}/run`, { method: "POST" }),
  history: (agentName: string) => fetchApi(`/api/agents/${agentName}/history`),
};

// ---------------------------------------------------------------------------
// Safety
// ---------------------------------------------------------------------------

export const safetyApi = {
  metrics: () => fetchApi<SafetyMetrics>("/api/safety/metrics"),
  osha300: () => fetchApi<OSHA300Record[]>("/api/safety/osha300"),
  inspections: () => fetchApi("/api/safety/inspections"),
  readinessScore: () => fetchApi<InspectionReadiness>("/api/safety/readiness-score"),
  contractors: () => fetchApi<ContractorSafetyProfile[]>("/api/safety/contractors"),
  exposure: () => fetchApi("/api/safety/exposure"),
};

// ---------------------------------------------------------------------------
// Commissioning
// ---------------------------------------------------------------------------

export const commissioningApi = {
  ist: () => fetchApi<ISTSequence[]>("/api/commissioning/ist"),
  punch: () => fetchApi<PunchItem[]>("/api/commissioning/punch"),
  turnover: () => fetchApi<TurnoverPackage[]>("/api/commissioning/turnover"),
};

// ---------------------------------------------------------------------------
// Environmental
// ---------------------------------------------------------------------------

export const environmentalApi = {
  permits: () => fetchApi<PermitStatus[]>("/api/environmental/permits"),
  leed: () => fetchApi<LEEDTracking>("/api/environmental/leed"),
  carbon: () => fetchApi("/api/environmental/carbon"),
};

// ---------------------------------------------------------------------------
// Claims
// ---------------------------------------------------------------------------

export const claimsApi = {
  timeline: () => fetchApi<ClaimEvent[]>("/api/claims/timeline"),
  notices: () => fetchApi<NoticeRecord[]>("/api/claims/notices"),
  delayAnalysis: () => fetchApi<DelayAnalysis>("/api/claims/delay-analysis"),
};

// ---------------------------------------------------------------------------
// Site Logistics
// ---------------------------------------------------------------------------

export const siteLogisticsApi = {
  crane: () => fetchApi<CraneScheduleEntry[]>("/api/site-logistics/crane"),
  staging: () => fetchApi<StagingPlan[]>("/api/site-logistics/staging"),
  headcount: () => fetchApi<SiteHeadcount>("/api/site-logistics/headcount"),
};
