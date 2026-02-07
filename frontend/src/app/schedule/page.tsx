"use client";

import { CriticalPathGantt } from "@/components/dashboard/CriticalPathGantt";
import { useAgentData } from "@/hooks/useAgentData";
import { scheduleApi } from "@/lib/api";
import type { CriticalPath, FloatReport, MonteCarloResult } from "@/lib/types";

const MOCK_CP: CriticalPath = {
  activities: [
    {
      id: "ACT-001",
      external_id: "A1010",
      name: "Foundation Pour - Zone A",
      start_date: "2025-03-01",
      end_date: "2025-03-15",
      total_float: 0.0,
      is_critical: true,
      tier_critical: true,
      predecessors: [],
      successors: ["ACT-002"],
    },
    {
      id: "ACT-002",
      external_id: "A1020",
      name: "Steel Erection - Zone A",
      start_date: "2025-03-16",
      end_date: "2025-04-15",
      total_float: 0.0,
      is_critical: true,
      tier_critical: true,
      predecessors: ["ACT-001"],
      successors: ["ACT-003"],
    },
  ],
  total_duration_days: 120,
  float_summary: { "Zone A": 0.0, "Zone B": 5.0 },
};

const MOCK_FLOAT: FloatReport[] = [
  {
    activity_id: "ACT-001",
    activity_name: "Foundation Pour - Zone A",
    total_float: 0.0,
    free_float: 0.0,
    status: "critical",
  },
  {
    activity_id: "ACT-003",
    activity_name: "MEP Rough-in - Zone B",
    total_float: 5.0,
    free_float: 3.0,
    status: "healthy",
  },
];

export default function SchedulePage() {
  const { data: cp } = useAgentData<CriticalPath>(scheduleApi.criticalPath);
  const { data: floatData } = useAgentData<FloatReport[]>(
    scheduleApi.floatReport,
  );

  const displayCp = cp ?? MOCK_CP;
  const displayFloat = floatData ?? MOCK_FLOAT;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Schedule Dashboard</h1>

      <CriticalPathGantt
        activities={displayCp.activities}
        totalDurationDays={displayCp.total_duration_days}
      />

      {/* Float Summary */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Float Summary
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {Object.entries(displayCp.float_summary).map(([zone, value]) => (
            <div
              key={zone}
              className={`p-3 rounded-lg ${
                value === 0
                  ? "bg-red-50 border border-red-200"
                  : value <= 5
                    ? "bg-amber-50 border border-amber-200"
                    : "bg-green-50 border border-green-200"
              }`}
            >
              <p className="text-sm font-medium">{zone}</p>
              <p
                className={`text-xl font-bold ${
                  value === 0
                    ? "text-danger"
                    : value <= 5
                      ? "text-warning"
                      : "text-success"
                }`}
              >
                {value} days
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Float Report Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Float Report
        </h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Activity
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Total Float
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Free Float
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {displayFloat.map((f) => (
              <tr
                key={f.activity_id}
                className="border-b border-gray-100 hover:bg-gray-50"
              >
                <td className="py-2 px-3 font-medium">{f.activity_name}</td>
                <td className="py-2 px-3 text-center">{f.total_float}d</td>
                <td className="py-2 px-3 text-center">{f.free_float}d</td>
                <td className="py-2 px-3 text-center">
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      f.status === "critical"
                        ? "bg-red-100 text-danger"
                        : f.status === "warning"
                          ? "bg-amber-100 text-amber-700"
                          : "bg-green-100 text-success"
                    }`}
                  >
                    {f.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
