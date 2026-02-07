"use client";

import { useState } from "react";
import type { DeviationTicket } from "@/lib/types";

interface ComplianceTicketListProps {
  tickets: DeviationTicket[];
}

const SEVERITY_COLORS: Record<string, string> = {
  critical: "bg-red-100 text-danger",
  major: "bg-orange-100 text-orange-700",
  minor: "bg-yellow-100 text-amber-700",
  info: "bg-blue-100 text-blue-700",
};

export function ComplianceTicketList({ tickets }: ComplianceTicketListProps) {
  const [sortBy, setSortBy] = useState<"severity" | "status">("severity");
  const [filterStatus, setFilterStatus] = useState<string>("all");

  const severityOrder: Record<string, number> = {
    critical: 0,
    major: 1,
    minor: 2,
    info: 3,
  };

  const filtered = tickets.filter(
    (t) => filterStatus === "all" || t.status === filterStatus,
  );

  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "severity") {
      return (severityOrder[a.severity] ?? 4) - (severityOrder[b.severity] ?? 4);
    }
    return a.status.localeCompare(b.status);
  });

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800">
          Compliance Tickets
        </h2>
        <div className="flex gap-2">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="text-xs border rounded px-2 py-1"
          >
            <option value="all">All Status</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "severity" | "status")}
            className="text-xs border rounded px-2 py-1"
          >
            <option value="severity">Sort: Severity</option>
            <option value="status">Sort: Status</option>
          </select>
        </div>
      </div>

      <div className="space-y-2">
        {sorted.map((ticket) => (
          <div
            key={ticket.id}
            className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
          >
            <span
              className={`text-xs px-2 py-0.5 rounded font-medium ${SEVERITY_COLORS[ticket.severity] ?? "bg-gray-100 text-gray-600"}`}
            >
              {ticket.severity}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-800 truncate">
                {ticket.title}
              </p>
              <p className="text-xs text-gray-500">{ticket.description}</p>
            </div>
            <span className="text-xs text-gray-500">{ticket.status}</span>
          </div>
        ))}
        {sorted.length === 0 && (
          <p className="text-sm text-gray-500 text-center py-4">
            No tickets found
          </p>
        )}
      </div>
    </div>
  );
}
