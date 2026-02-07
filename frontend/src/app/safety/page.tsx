"use client";

import { SafetyDashboard } from "@/components/dashboard/SafetyDashboard";
import { OSHA300Table } from "@/components/dashboard/OSHA300Table";
import { useAgentData } from "@/hooks/useAgentData";
import { safetyApi } from "@/lib/api";
import type {
  SafetyMetrics,
  OSHA300Record,
  InspectionReadiness,
  ContractorSafetyProfile,
} from "@/lib/types";

const MOCK_METRICS: SafetyMetrics = {
  trir: 1.8,
  dart: 0.9,
  emr: 0.85,
  days_since_recordable: 45,
  near_misses_ytd: 12,
  first_aid_ytd: 8,
  recordables_ytd: 2,
  man_hours_ytd: 220000,
};

const MOCK_OSHA: OSHA300Record[] = [
  {
    case_number: "2025-001",
    employee: "Worker A",
    date_of_injury: "2025-01-12",
    description: "Struck by falling debris",
    classification: "recordable",
    days_away: 3,
    days_restricted: 5,
    body_part: "Left shoulder",
  },
  {
    case_number: "2025-002",
    employee: "Worker B",
    date_of_injury: "2025-01-28",
    description: "Slip on wet surface",
    classification: "first_aid",
    days_away: 0,
    days_restricted: 0,
    body_part: "Right knee",
  },
];

const MOCK_CONTRACTORS: ContractorSafetyProfile[] = [
  {
    contractor: "SteelWorks LLC",
    emr: 0.78,
    trir: 1.2,
    prequalified: true,
    incidents_ytd: 0,
    training_compliance_pct: 100,
  },
  {
    contractor: "MechCo Inc",
    emr: 0.92,
    trir: 2.1,
    prequalified: true,
    incidents_ytd: 1,
    training_compliance_pct: 95,
  },
];

export default function SafetyPage() {
  const { data: metrics } = useAgentData<SafetyMetrics>(safetyApi.metrics);
  const { data: osha } = useAgentData<OSHA300Record[]>(safetyApi.osha300);
  const { data: readiness } = useAgentData<InspectionReadiness>(
    safetyApi.readinessScore,
  );
  const { data: contractors } = useAgentData<ContractorSafetyProfile[]>(
    safetyApi.contractors,
  );

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Safety Dashboard</h1>

      <SafetyDashboard
        metrics={metrics ?? MOCK_METRICS}
        contractors={contractors ?? MOCK_CONTRACTORS}
        readinessScore={readiness?.overall_score ?? 87}
      />

      <OSHA300Table records={osha ?? MOCK_OSHA} />
    </div>
  );
}
