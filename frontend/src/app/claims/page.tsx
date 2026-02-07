"use client";

import { useAgentData } from "@/hooks/useAgentData";
import { claimsApi } from "@/lib/api";
import type { ClaimEvent, NoticeRecord, DelayAnalysis } from "@/lib/types";

const MOCK_CLAIMS: ClaimEvent[] = [
  {
    id: "CLM-001",
    title: "Differing site conditions - Zone A",
    type: "differing_conditions",
    amount: 350000,
    filed_date: "2025-01-15",
    status: "under_review",
    milestones: [
      { date: "2025-01-10", event: "Notice of claim filed" },
      { date: "2025-01-15", event: "Supporting docs submitted" },
      { date: "2025-02-01", event: "Owner review in progress" },
    ],
  },
];

const MOCK_NOTICES: NoticeRecord[] = [
  {
    id: "NOT-001",
    notice_type: "delay",
    from_party: "GC",
    to_party: "Owner",
    subject: "Weather delay notice - January storms",
    sent_date: "2025-01-20",
    response_due: "2025-02-03",
    status: "awaiting_response",
  },
  {
    id: "NOT-002",
    notice_type: "change",
    from_party: "GC",
    to_party: "SubA",
    subject: "Scope change - MEP reroute",
    sent_date: "2025-01-25",
    response_due: "2025-02-08",
    status: "acknowledged",
  },
];

const MOCK_DELAY: DelayAnalysis = {
  method: "time_impact_analysis",
  baseline_completion: "2025-12-01",
  projected_completion: "2026-01-15",
  total_delay_days: 45,
  excusable_days: 30,
  non_excusable_days: 15,
  compensable_days: 20,
  delay_events: [
    {
      id: "DE-001",
      description: "Unforeseen rock removal",
      delay_days: 14,
      excusable: true,
      compensable: true,
    },
    {
      id: "DE-002",
      description: "Abnormal rainfall January",
      delay_days: 10,
      excusable: true,
      compensable: false,
    },
    {
      id: "DE-003",
      description: "Late submittal turnaround",
      delay_days: 7,
      excusable: false,
      compensable: false,
    },
  ],
};

export default function ClaimsPage() {
  const { data: claims } = useAgentData<ClaimEvent[]>(claimsApi.timeline);
  const { data: notices } = useAgentData<NoticeRecord[]>(claimsApi.notices);
  const { data: delay } = useAgentData<DelayAnalysis>(
    claimsApi.delayAnalysis,
  );

  const displayClaims = claims ?? MOCK_CLAIMS;
  const displayNotices = notices ?? MOCK_NOTICES;
  const displayDelay = delay ?? MOCK_DELAY;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Claims Dashboard</h1>

      {/* Claims Timeline */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Claims Timeline
        </h2>
        <div className="space-y-4">
          {displayClaims.map((claim) => (
            <div key={claim.id} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <h3 className="text-sm font-semibold text-gray-800">
                    {claim.title}
                  </h3>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs px-2 py-0.5 bg-gray-200 rounded">
                      {claim.type.replace("_", " ")}
                    </span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded font-medium ${
                        claim.status === "under_review"
                          ? "bg-amber-100 text-amber-700"
                          : claim.status === "approved"
                            ? "bg-green-100 text-success"
                            : "bg-gray-100 text-gray-500"
                      }`}
                    >
                      {claim.status.replace("_", " ")}
                    </span>
                  </div>
                </div>
                <span className="text-lg font-bold text-gray-800">
                  ${claim.amount.toLocaleString()}
                </span>
              </div>
              {/* Milestone timeline */}
              <div className="mt-3 pl-3 border-l-2 border-gray-300 space-y-2">
                {claim.milestones.map((ms, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <span className="text-xs text-gray-500 w-20 flex-shrink-0">
                      {ms.date}
                    </span>
                    <span className="text-xs text-gray-700">{ms.event}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Notices */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Notices</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 px-3 text-gray-500 font-medium">Type</th>
                <th className="text-left py-2 px-3 text-gray-500 font-medium">Subject</th>
                <th className="text-left py-2 px-3 text-gray-500 font-medium">From / To</th>
                <th className="text-left py-2 px-3 text-gray-500 font-medium">Due</th>
                <th className="text-center py-2 px-3 text-gray-500 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {displayNotices.map((notice) => (
                <tr
                  key={notice.id}
                  className="border-b border-gray-100 hover:bg-gray-50"
                >
                  <td className="py-2 px-3">
                    <span className="text-xs px-2 py-0.5 bg-gray-200 rounded">
                      {notice.notice_type}
                    </span>
                  </td>
                  <td className="py-2 px-3">{notice.subject}</td>
                  <td className="py-2 px-3 text-gray-600">
                    {notice.from_party} to {notice.to_party}
                  </td>
                  <td className="py-2 px-3 text-gray-600">{notice.response_due}</td>
                  <td className="py-2 px-3 text-center">
                    <span
                      className={`text-xs px-2 py-0.5 rounded font-medium ${
                        notice.status === "awaiting_response"
                          ? "bg-amber-100 text-amber-700"
                          : notice.status === "acknowledged"
                            ? "bg-green-100 text-success"
                            : "bg-gray-100 text-gray-500"
                      }`}
                    >
                      {notice.status.replace("_", " ")}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Delay Analysis */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Delay Analysis
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <p className="text-xs text-gray-500">Total Delay</p>
            <p className="text-xl font-bold text-danger">
              {displayDelay.total_delay_days}d
            </p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <p className="text-xs text-gray-500">Excusable</p>
            <p className="text-xl font-bold text-warning">
              {displayDelay.excusable_days}d
            </p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <p className="text-xs text-gray-500">Non-Excusable</p>
            <p className="text-xl font-bold text-gray-700">
              {displayDelay.non_excusable_days}d
            </p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <p className="text-xs text-gray-500">Compensable</p>
            <p className="text-xl font-bold text-success">
              {displayDelay.compensable_days}d
            </p>
          </div>
        </div>
        <div className="space-y-2">
          {displayDelay.delay_events.map((de) => (
            <div
              key={de.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
            >
              <span className="text-sm font-bold text-gray-700 w-8">
                {de.delay_days}d
              </span>
              <p className="text-sm text-gray-700 flex-1">{de.description}</p>
              <div className="flex gap-2">
                <span
                  className={`text-xs px-2 py-0.5 rounded ${
                    de.excusable ? "bg-green-100 text-success" : "bg-red-100 text-danger"
                  }`}
                >
                  {de.excusable ? "Excusable" : "Non-excusable"}
                </span>
                {de.compensable && (
                  <span className="text-xs px-2 py-0.5 bg-blue-100 text-primary rounded">
                    Compensable
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
