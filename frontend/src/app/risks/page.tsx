"use client";

import { RiskHeatMap } from "@/components/dashboard/RiskHeatMap";
import { useAgentData } from "@/hooks/useAgentData";
import { risksApi } from "@/lib/api";
import type { RiskEvent, RiskHeatMapCell } from "@/lib/types";

const MOCK_RISKS: RiskEvent[] = [
  {
    id: "RISK-001",
    project_id: "default-project",
    category: "weather",
    description: "Hurricane season risk to exterior work",
    risk_score: {
      probability: 0.35,
      impact_dollars: 500000,
      impact_days: 14,
      safety_critical: false,
      composite_score: 175000,
    },
    confidence: 0.82,
    data_sources: [],
    transparency_log: ["Checked NOAA 14-day forecast"],
    status: "active",
    created_at: "2025-01-15T00:00:00Z",
    updated_at: null,
  },
];

const MOCK_HEATMAP: RiskHeatMapCell[] = [
  {
    probability_range: "0.3-0.5",
    impact_range: "$250k-$500k",
    count: 2,
    risk_ids: ["RISK-001", "RISK-003"],
  },
  {
    probability_range: "0.1-0.3",
    impact_range: "$100k-$250k",
    count: 1,
    risk_ids: ["RISK-002"],
  },
];

export default function RisksPage() {
  const { data: risks } = useAgentData<RiskEvent[]>(risksApi.list);
  const { data: heatmapData } = useAgentData(risksApi.heatmap);

  const displayRisks = risks ?? MOCK_RISKS;
  const displayHeatmap =
    (heatmapData as { cells: RiskHeatMapCell[] })?.cells ?? MOCK_HEATMAP;

  const sorted = [...displayRisks].sort(
    (a, b) => b.risk_score.composite_score - a.risk_score.composite_score,
  );

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Risk Dashboard</h1>

      <RiskHeatMap cells={displayHeatmap} />

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Active Risks (by composite score)
        </h2>
        <div className="space-y-3">
          {sorted.map((risk) => (
            <div
              key={risk.id}
              className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex-shrink-0 text-center">
                <p className="text-xs text-gray-500">Score</p>
                <p className="text-lg font-bold text-danger">
                  {(risk.risk_score.composite_score / 1000).toFixed(0)}K
                </p>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs px-2 py-0.5 rounded bg-gray-200 font-medium">
                    {risk.category}
                  </span>
                  <span className="text-xs text-gray-500">{risk.id}</span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      risk.risk_score.safety_critical
                        ? "bg-red-100 text-danger"
                        : "bg-gray-100 text-gray-500"
                    }`}
                  >
                    {risk.risk_score.safety_critical
                      ? "Safety Critical"
                      : "Non-Safety"}
                  </span>
                </div>
                <p className="text-sm text-gray-800">{risk.description}</p>
                <div className="flex gap-4 mt-2 text-xs text-gray-500">
                  <span>
                    P: {(risk.risk_score.probability * 100).toFixed(0)}%
                  </span>
                  <span>
                    Cost: ${(risk.risk_score.impact_dollars / 1000).toFixed(0)}K
                  </span>
                  <span>Days: {risk.risk_score.impact_days}</span>
                  <span>
                    Conf: {(risk.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
