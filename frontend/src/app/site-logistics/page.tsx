"use client";

import { useAgentData } from "@/hooks/useAgentData";
import { siteLogisticsApi } from "@/lib/api";
import type { CraneScheduleEntry, StagingPlan, SiteHeadcount } from "@/lib/types";

const MOCK_CRANE: CraneScheduleEntry[] = [
  {
    id: "CR-001",
    crane_id: "Tower Crane TC-1",
    date: "2025-02-03",
    time_slots: [
      { start: "07:00", end: "10:00", trade: "Ironworkers", description: "Steel erection L3" },
      { start: "10:30", end: "12:00", trade: "Concrete", description: "Bucket pour L2" },
      { start: "13:00", end: "15:30", trade: "MEP", description: "AHU lift L4" },
    ],
  },
];

const MOCK_STAGING: StagingPlan[] = [
  {
    id: "SZ-001",
    zone: "North Laydown",
    capacity_pct: 75,
    current_materials: ["Structural steel - 40 tons", "Rebar bundles - 200 pcs"],
    reserved_until: "2025-02-10",
    status: "active",
  },
  {
    id: "SZ-002",
    zone: "South Staging",
    capacity_pct: 30,
    current_materials: ["Drywall - 500 sheets"],
    reserved_until: "2025-02-15",
    status: "active",
  },
];

const MOCK_HEADCOUNT: SiteHeadcount = {
  date: "2025-02-03",
  total: 156,
  by_trade: [
    { trade: "Ironworkers", count: 24 },
    { trade: "Electricians", count: 18 },
    { trade: "Plumbers", count: 14 },
    { trade: "Concrete", count: 20 },
    { trade: "Carpenters", count: 16 },
    { trade: "Laborers", count: 32 },
    { trade: "MEP", count: 22 },
    { trade: "Supervision", count: 10 },
  ],
};

export default function SiteLogisticsPage() {
  const { data: crane } = useAgentData<CraneScheduleEntry[]>(
    siteLogisticsApi.crane,
  );
  const { data: staging } = useAgentData<StagingPlan[]>(
    siteLogisticsApi.staging,
  );
  const { data: headcount } = useAgentData<SiteHeadcount>(
    siteLogisticsApi.headcount,
  );

  const displayCrane = crane ?? MOCK_CRANE;
  const displayStaging = staging ?? MOCK_STAGING;
  const displayHeadcount = headcount ?? MOCK_HEADCOUNT;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Site Logistics Dashboard
      </h1>

      {/* Crane Schedule */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Crane Schedule
        </h2>
        {displayCrane.map((entry) => (
          <div key={entry.id} className="mb-4">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm font-medium text-gray-800">
                {entry.crane_id}
              </span>
              <span className="text-xs text-gray-500">{entry.date}</span>
            </div>
            <div className="space-y-2">
              {entry.time_slots.map((slot, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
                >
                  <span className="text-sm font-mono text-gray-600 w-28 flex-shrink-0">
                    {slot.start} - {slot.end}
                  </span>
                  <span className="text-xs px-2 py-0.5 bg-primary/10 text-primary rounded font-medium">
                    {slot.trade}
                  </span>
                  <span className="text-sm text-gray-700">
                    {slot.description}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Staging Zones */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Staging Zones
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {displayStaging.map((zone) => (
            <div
              key={zone.id}
              className="p-4 border border-gray-100 rounded-lg"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-gray-800">
                  {zone.zone}
                </span>
                <span
                  className={`text-sm font-bold ${
                    zone.capacity_pct >= 80
                      ? "text-danger"
                      : zone.capacity_pct >= 60
                        ? "text-warning"
                        : "text-success"
                  }`}
                >
                  {zone.capacity_pct}% full
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div
                  className={`h-2 rounded-full ${
                    zone.capacity_pct >= 80
                      ? "bg-danger"
                      : zone.capacity_pct >= 60
                        ? "bg-warning"
                        : "bg-success"
                  }`}
                  style={{ width: `${zone.capacity_pct}%` }}
                />
              </div>
              <ul className="text-xs text-gray-500 space-y-0.5">
                {zone.current_materials.map((mat, i) => (
                  <li key={i}>- {mat}</li>
                ))}
              </ul>
              <p className="text-xs text-gray-400 mt-1">
                Reserved until {zone.reserved_until}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Site Headcount */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">
            Site Headcount
          </h2>
          <div className="text-right">
            <span className="text-2xl font-bold text-primary">
              {displayHeadcount.total}
            </span>
            <p className="text-xs text-gray-500">{displayHeadcount.date}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {displayHeadcount.by_trade.map((t) => (
            <div
              key={t.trade}
              className="p-3 bg-gray-50 rounded-lg text-center"
            >
              <p className="text-xs text-gray-500">{t.trade}</p>
              <p className="text-xl font-bold text-gray-800">{t.count}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
