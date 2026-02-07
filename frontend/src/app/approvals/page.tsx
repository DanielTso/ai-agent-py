"use client";

import { ApprovalCard } from "@/components/dashboard/ApprovalCard";
import { useApprovals } from "@/hooks/useApprovals";
import type { ApprovalRequest } from "@/lib/types";

const MOCK_APPROVALS: ApprovalRequest[] = [
  {
    id: "APR-001",
    agent_name: "supply_chain",
    action_type: "expedite_vendor",
    title: "Expedite steel delivery via SteelWorks USA",
    description:
      "Current vendor delayed 10 days. Alternative vendor can deliver 5 days sooner at $25K premium.",
    confidence: 85,
    data_sources: [],
    transparency_log: [
      "Checked 3 alternative vendors",
      "Verified schedule impact with critical path",
      "Cost within contingency budget",
    ],
    impact: {
      cost_delta: 25000,
      schedule_delta_days: -5,
      risk_change: "reduced",
      description: "Net schedule improvement of 5 days",
    },
    status: "pending",
    pm_notes: null,
  },
];

export default function ApprovalsPage() {
  const { approvals, loading, approve, reject } = useApprovals();

  const displayApprovals =
    approvals.length > 0 ? approvals : MOCK_APPROVALS;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Approvals</h1>
        <span className="text-sm text-gray-500">
          {displayApprovals.filter((a) => a.status === "pending").length} pending
        </span>
      </div>

      {loading && (
        <p className="text-sm text-gray-500">Loading approvals...</p>
      )}

      <div className="space-y-4">
        {displayApprovals.map((approval) => (
          <ApprovalCard
            key={approval.id}
            approval={approval}
            onApprove={approve}
            onReject={reject}
          />
        ))}
      </div>

      {displayApprovals.length === 0 && !loading && (
        <div className="text-center py-12 text-gray-500">
          <p>No approvals found</p>
        </div>
      )}
    </div>
  );
}
