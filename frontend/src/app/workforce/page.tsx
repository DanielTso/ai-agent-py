"use client";

import { useAgentData } from "@/hooks/useAgentData";
import { workforceApi } from "@/lib/api";
import type { CrewStatus, ProductivityMetric, CertificationRecord } from "@/lib/types";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

const MOCK_CREWS: CrewStatus[] = [
  {
    trade: "Ironworkers",
    headcount: 24,
    planned_production: 1200,
    actual_production: 1100,
    productivity_pct: 91.7,
    location: "Level 3, Zone A",
    overtime_hours: 16,
  },
  {
    trade: "Electricians",
    headcount: 18,
    planned_production: 800,
    actual_production: 820,
    productivity_pct: 102.5,
    location: "Level 2, Zone B",
    overtime_hours: 4,
  },
];

const MOCK_PRODUCTIVITY: ProductivityMetric[] = [
  {
    trade: "Ironworkers",
    period: "2025-W05",
    planned_units: 300,
    actual_units: 275,
    productivity_index: 0.917,
    trend: "stable",
  },
  {
    trade: "Electricians",
    period: "2025-W05",
    planned_units: 200,
    actual_units: 205,
    productivity_index: 1.025,
    trend: "improving",
  },
];

const MOCK_CERTS: CertificationRecord[] = [
  {
    worker_id: "W-101",
    worker_name: "John Smith",
    cert_type: "OSHA30",
    issue_date: "2023-06-15",
    expiry_date: "2025-06-15",
    status: "valid",
  },
  {
    worker_id: "W-102",
    worker_name: "Maria Garcia",
    cert_type: "NETA",
    issue_date: "2022-03-10",
    expiry_date: "2025-03-10",
    status: "expiring_soon",
  },
];

const TrendIcon = ({ trend }: { trend: string }) => {
  if (trend === "improving") return <TrendingUp size={14} className="text-success" />;
  if (trend === "declining") return <TrendingDown size={14} className="text-danger" />;
  return <Minus size={14} className="text-gray-400" />;
};

export default function WorkforcePage() {
  const { data: crews } = useAgentData<CrewStatus[]>(workforceApi.crews);
  const { data: productivity } = useAgentData<ProductivityMetric[]>(
    workforceApi.productivity,
  );
  const { data: certs } = useAgentData<CertificationRecord[]>(
    workforceApi.certs,
  );

  const displayCrews = crews ?? MOCK_CREWS;
  const displayProd = productivity ?? MOCK_PRODUCTIVITY;
  const displayCerts = certs ?? MOCK_CERTS;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Workforce Dashboard
      </h1>

      {/* Crew Status */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Crew Status
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 px-3 text-gray-500 font-medium">Trade</th>
                <th className="text-center py-2 px-3 text-gray-500 font-medium">Headcount</th>
                <th className="text-center py-2 px-3 text-gray-500 font-medium">Productivity</th>
                <th className="text-left py-2 px-3 text-gray-500 font-medium">Location</th>
                <th className="text-center py-2 px-3 text-gray-500 font-medium">OT Hours</th>
              </tr>
            </thead>
            <tbody>
              {displayCrews.map((crew) => (
                <tr key={crew.trade} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-2 px-3 font-medium">{crew.trade}</td>
                  <td className="py-2 px-3 text-center">{crew.headcount}</td>
                  <td className="py-2 px-3 text-center">
                    <span
                      className={`font-medium ${
                        crew.productivity_pct >= 100
                          ? "text-success"
                          : crew.productivity_pct >= 90
                            ? "text-warning"
                            : "text-danger"
                      }`}
                    >
                      {crew.productivity_pct.toFixed(1)}%
                    </span>
                  </td>
                  <td className="py-2 px-3 text-gray-600">{crew.location ?? "-"}</td>
                  <td className="py-2 px-3 text-center">{crew.overtime_hours}h</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Productivity */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Productivity Metrics
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {displayProd.map((p) => (
            <div key={`${p.trade}-${p.period}`} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">{p.trade}</span>
                <div className="flex items-center gap-1">
                  <TrendIcon trend={p.trend} />
                  <span className="text-xs text-gray-500">{p.trend}</span>
                </div>
              </div>
              <p className="text-xl font-bold text-gray-800">
                {p.productivity_index.toFixed(3)}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {p.actual_units}/{p.planned_units} units ({p.period})
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Certifications */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Certifications
        </h2>
        <div className="space-y-2">
          {displayCerts.map((cert) => (
            <div
              key={`${cert.worker_id}-${cert.cert_type}`}
              className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex-1">
                <p className="text-sm font-medium">{cert.worker_name}</p>
                <p className="text-xs text-gray-500">{cert.cert_type}</p>
              </div>
              <p className="text-xs text-gray-500">
                Expires: {cert.expiry_date ?? "N/A"}
              </p>
              <span
                className={`text-xs px-2 py-0.5 rounded font-medium ${
                  cert.status === "valid"
                    ? "bg-green-100 text-success"
                    : cert.status === "expiring_soon"
                      ? "bg-amber-100 text-amber-700"
                      : "bg-red-100 text-danger"
                }`}
              >
                {cert.status.replace("_", " ")}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
