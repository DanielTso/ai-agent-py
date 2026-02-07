"use client";

import { ComplianceTicketList } from "@/components/dashboard/ComplianceTicketList";
import { useAgentData } from "@/hooks/useAgentData";
import { complianceApi } from "@/lib/api";
import type { DeviationTicket } from "@/lib/types";

const MOCK_TICKETS: DeviationTicket[] = [
  {
    id: "DT-001",
    compliance_check_id: "CC-001",
    title: "Wall thickness deviation at A-3",
    description: "BIM model shows 6in wall but field measurement is 4.5in",
    severity: "major",
    bim_overlay_url: null,
    assigned_to: "Field Engineer",
    due_date: null,
    status: "open",
  },
];

export default function CompliancePage() {
  const { data: tickets } = useAgentData<DeviationTicket[]>(
    complianceApi.tickets,
  );
  const { data: summary } = useAgentData(complianceApi.summary);

  const displayTickets = tickets ?? MOCK_TICKETS;
  const stats = (summary as Record<string, number>) ?? {
    total_checks: 42,
    open: 5,
    in_progress: 3,
    resolved: 30,
    critical: 1,
    major: 3,
    minor: 1,
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Compliance Dashboard
      </h1>

      {/* Summary cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        {Object.entries(stats).map(([key, value]) => (
          <div
            key={key}
            className="bg-white rounded-lg border border-gray-200 p-3 text-center"
          >
            <p className="text-xs text-gray-500 capitalize">
              {key.replace("_", " ")}
            </p>
            <p
              className={`text-xl font-bold ${
                key === "critical"
                  ? "text-danger"
                  : key === "major"
                    ? "text-warning"
                    : "text-gray-800"
              }`}
            >
              {value}
            </p>
          </div>
        ))}
      </div>

      <ComplianceTicketList tickets={displayTickets} />
    </div>
  );
}
