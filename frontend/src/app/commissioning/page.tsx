"use client";

import { useAgentData } from "@/hooks/useAgentData";
import { commissioningApi } from "@/lib/api";
import type { ISTSequence, PunchItem, TurnoverPackage } from "@/lib/types";

const MOCK_IST: ISTSequence[] = [
  {
    id: "IST-001",
    system: "HVAC - AHU-1",
    status: "in_progress",
    progress_pct: 65,
    tests_passed: 8,
    tests_total: 12,
    next_test: "Supply air balance verification",
  },
  {
    id: "IST-002",
    system: "Fire Alarm - Zone 1",
    status: "pending",
    progress_pct: 0,
    tests_passed: 0,
    tests_total: 15,
    next_test: "Initiating device verification",
  },
];

const MOCK_PUNCH: PunchItem[] = [
  {
    id: "PL-001",
    description: "Damper actuator not responding",
    system: "HVAC",
    location: "Level 3, Mechanical Room",
    severity: "major",
    assigned_to: "MechCo LLC",
    status: "open",
  },
  {
    id: "PL-002",
    description: "Missing fire caulk at penetration",
    system: "Fire Protection",
    location: "Level 2, Grid B-4",
    severity: "critical",
    assigned_to: "FireStop Inc",
    status: "in_progress",
  },
];

const MOCK_TURNOVER: TurnoverPackage[] = [
  {
    id: "TO-001",
    system: "HVAC",
    documents_complete: 12,
    documents_required: 18,
    progress_pct: 66.7,
    status: "in_progress",
    missing: ["TAB report", "Sequence of operations", "Training records"],
  },
  {
    id: "TO-002",
    system: "Electrical",
    documents_complete: 20,
    documents_required: 20,
    progress_pct: 100.0,
    status: "complete",
    missing: [],
  },
];

export default function CommissioningPage() {
  const { data: ist } = useAgentData<ISTSequence[]>(commissioningApi.ist);
  const { data: punch } = useAgentData<PunchItem[]>(commissioningApi.punch);
  const { data: turnover } = useAgentData<TurnoverPackage[]>(
    commissioningApi.turnover,
  );

  const displayIST = ist ?? MOCK_IST;
  const displayPunch = punch ?? MOCK_PUNCH;
  const displayTurnover = turnover ?? MOCK_TURNOVER;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Commissioning Dashboard
      </h1>

      {/* IST Sequence */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Integrated System Testing
        </h2>
        <div className="space-y-3">
          {displayIST.map((test) => (
            <div key={test.id} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <span className="text-sm font-medium text-gray-800">
                    {test.system}
                  </span>
                  <span
                    className={`ml-2 text-xs px-2 py-0.5 rounded font-medium ${
                      test.status === "completed"
                        ? "bg-green-100 text-success"
                        : test.status === "in_progress"
                          ? "bg-blue-100 text-primary"
                          : test.status === "blocked"
                            ? "bg-red-100 text-danger"
                            : "bg-gray-100 text-gray-500"
                    }`}
                  >
                    {test.status.replace("_", " ")}
                  </span>
                </div>
                <span className="text-sm font-bold text-gray-700">
                  {test.tests_passed}/{test.tests_total}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all"
                  style={{ width: `${test.progress_pct}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Next: {test.next_test}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Punch List */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Punch List
        </h2>
        <div className="space-y-2">
          {displayPunch.map((item) => (
            <div
              key={item.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
            >
              <span
                className={`text-xs px-2 py-0.5 rounded font-medium ${
                  item.severity === "critical"
                    ? "bg-red-100 text-danger"
                    : item.severity === "major"
                      ? "bg-orange-100 text-orange-700"
                      : "bg-gray-100 text-gray-600"
                }`}
              >
                {item.severity}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-800 truncate">
                  {item.description}
                </p>
                <p className="text-xs text-gray-500">
                  {item.system} - {item.location}
                </p>
              </div>
              <span className="text-xs text-gray-500">{item.assigned_to}</span>
              <span className="text-xs text-gray-400">{item.status}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Turnover Packages */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Turnover Packages
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {displayTurnover.map((pkg) => (
            <div
              key={pkg.id}
              className="p-4 border border-gray-100 rounded-lg"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold">{pkg.system}</span>
                <span
                  className={`text-xs px-2 py-0.5 rounded font-medium ${
                    pkg.status === "complete"
                      ? "bg-green-100 text-success"
                      : "bg-amber-100 text-amber-700"
                  }`}
                >
                  {pkg.progress_pct.toFixed(0)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div
                  className={`h-2 rounded-full ${
                    pkg.progress_pct >= 100 ? "bg-success" : "bg-primary"
                  }`}
                  style={{ width: `${pkg.progress_pct}%` }}
                />
              </div>
              <p className="text-xs text-gray-500">
                {pkg.documents_complete}/{pkg.documents_required} documents
              </p>
              {pkg.missing.length > 0 && (
                <div className="mt-2">
                  <p className="text-xs text-danger font-medium">Missing:</p>
                  <ul className="text-xs text-gray-500 mt-1">
                    {pkg.missing.map((doc, i) => (
                      <li key={i}>- {doc}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
