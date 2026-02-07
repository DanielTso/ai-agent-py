"use client";

import { useState } from "react";
import { CheckCircle2, XCircle, ChevronDown, ChevronUp } from "lucide-react";
import type { ApprovalRequest } from "@/lib/types";

interface ApprovalCardProps {
  approval: ApprovalRequest;
  onApprove: (id: string, notes: string) => void;
  onReject: (id: string, notes: string) => void;
}

export function ApprovalCard({
  approval,
  onApprove,
  onReject,
}: ApprovalCardProps) {
  const [notes, setNotes] = useState("");
  const [expanded, setExpanded] = useState(false);

  const isPending = approval.status === "pending";

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-5">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs px-2 py-0.5 rounded bg-primary/10 text-primary font-medium">
              {approval.agent_name}
            </span>
            <span className="text-xs text-gray-500">
              {approval.action_type}
            </span>
            <span
              className={`text-xs px-2 py-0.5 rounded font-medium ${
                approval.status === "approved"
                  ? "bg-green-100 text-success"
                  : approval.status === "rejected"
                    ? "bg-red-100 text-danger"
                    : "bg-amber-100 text-amber-700"
              }`}
            >
              {approval.status}
            </span>
          </div>
          <h3 className="text-sm font-semibold text-gray-900">
            {approval.title}
          </h3>
          <p className="text-sm text-gray-600 mt-1">{approval.description}</p>
        </div>
        <span className="text-xs text-gray-500 ml-4 flex-shrink-0">
          {approval.confidence}% confidence
        </span>
      </div>

      {/* Impact */}
      <div className="flex gap-4 mt-3">
        <span
          className={`text-xs font-medium ${approval.impact.cost_delta > 0 ? "text-danger" : "text-success"}`}
        >
          Cost: {approval.impact.cost_delta > 0 ? "+" : ""}$
          {approval.impact.cost_delta.toLocaleString()}
        </span>
        <span
          className={`text-xs font-medium ${approval.impact.schedule_delta_days > 0 ? "text-danger" : "text-success"}`}
        >
          Schedule: {approval.impact.schedule_delta_days > 0 ? "+" : ""}
          {approval.impact.schedule_delta_days}d
        </span>
      </div>

      {/* Expandable transparency log */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1 mt-3 text-xs text-gray-500 hover:text-gray-700"
      >
        {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        Transparency Log ({approval.transparency_log.length} entries)
      </button>

      {expanded && (
        <div className="mt-2 p-3 bg-gray-50 rounded text-xs space-y-1">
          {approval.transparency_log.map((entry, i) => (
            <p key={i} className="text-gray-600">
              - {entry}
            </p>
          ))}
        </div>
      )}

      {/* Actions */}
      {isPending && (
        <div className="mt-4 pt-3 border-t border-gray-100">
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add notes (optional)..."
            className="w-full text-sm border rounded-lg p-2 mb-2 resize-none h-16"
          />
          <div className="flex gap-2">
            <button
              onClick={() => onApprove(approval.id, notes)}
              className="flex items-center gap-1 px-4 py-2 bg-success text-white text-sm rounded-lg hover:bg-success/90 transition-colors"
            >
              <CheckCircle2 size={16} />
              Approve
            </button>
            <button
              onClick={() => onReject(approval.id, notes)}
              className="flex items-center gap-1 px-4 py-2 bg-danger text-white text-sm rounded-lg hover:bg-danger/90 transition-colors"
            >
              <XCircle size={16} />
              Reject
            </button>
          </div>
        </div>
      )}

      {/* PM Notes (if already decided) */}
      {!isPending && approval.pm_notes && (
        <div className="mt-3 p-3 bg-gray-50 rounded">
          <p className="text-xs text-gray-500">PM Notes:</p>
          <p className="text-sm text-gray-700">{approval.pm_notes}</p>
        </div>
      )}
    </div>
  );
}
