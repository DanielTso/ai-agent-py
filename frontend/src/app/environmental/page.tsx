"use client";

import { useAgentData } from "@/hooks/useAgentData";
import { environmentalApi } from "@/lib/api";
import type { PermitStatus, LEEDTracking } from "@/lib/types";

const MOCK_PERMITS: PermitStatus[] = [
  {
    id: "EP-001",
    permit_type: "SWPPP",
    description: "Stormwater Pollution Prevention Plan",
    status: "active",
    expiry_date: "2025-12-31",
    inspector: "EPA Region 4",
    last_inspection: "2025-01-15",
  },
  {
    id: "EP-002",
    permit_type: "Air Quality",
    description: "Dust control permit",
    status: "active",
    expiry_date: "2025-06-30",
    inspector: "State DEQ",
    last_inspection: "2025-01-20",
  },
];

const MOCK_LEED: LEEDTracking = {
  target_level: "Gold",
  current_points: 52,
  target_points: 60,
  categories: [
    { name: "Energy & Atmosphere", earned: 18, possible: 33 },
    { name: "Materials & Resources", earned: 8, possible: 13 },
    { name: "Water Efficiency", earned: 7, possible: 11 },
    { name: "Indoor Environmental Quality", earned: 10, possible: 16 },
    { name: "Sustainable Sites", earned: 9, possible: 26 },
  ],
};

export default function EnvironmentalPage() {
  const { data: permits } = useAgentData<PermitStatus[]>(
    environmentalApi.permits,
  );
  const { data: leed } = useAgentData<LEEDTracking>(environmentalApi.leed);

  const displayPermits = permits ?? MOCK_PERMITS;
  const displayLeed = leed ?? MOCK_LEED;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Environmental Dashboard
      </h1>

      {/* Permits */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Environmental Permits
        </h2>
        <div className="space-y-3">
          {displayPermits.map((permit) => (
            <div
              key={permit.id}
              className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-medium text-gray-800">
                    {permit.permit_type}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      permit.status === "active"
                        ? "bg-green-100 text-success"
                        : permit.status === "expiring"
                          ? "bg-amber-100 text-amber-700"
                          : "bg-red-100 text-danger"
                    }`}
                  >
                    {permit.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{permit.description}</p>
              </div>
              <div className="text-right text-xs text-gray-500">
                <p>Expires: {permit.expiry_date}</p>
                <p>Last inspection: {permit.last_inspection}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* LEED Tracking */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">
            LEED Tracking
          </h2>
          <span className="text-sm font-medium text-primary">
            Target: {displayLeed.target_level} ({displayLeed.target_points} pts)
          </span>
        </div>

        {/* Overall Progress */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm text-gray-600">
              {displayLeed.current_points} / {displayLeed.target_points} points
            </span>
            <span className="text-sm font-bold text-primary">
              {((displayLeed.current_points / displayLeed.target_points) * 100).toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-success h-3 rounded-full transition-all"
              style={{
                width: `${(displayLeed.current_points / displayLeed.target_points) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* Category Breakdown */}
        <div className="space-y-3">
          {displayLeed.categories.map((cat) => (
            <div key={cat.name}>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-gray-700">{cat.name}</span>
                <span className="text-gray-500">
                  {cat.earned}/{cat.possible}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-light h-2 rounded-full"
                  style={{
                    width: `${(cat.earned / cat.possible) * 100}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
