"use client";

import { DailyBriefCard } from "@/components/dashboard/DailyBriefCard";
import { useAgentData } from "@/hooks/useAgentData";
import { briefsApi, agentsApi, approvalsApi } from "@/lib/api";
import { Bot, CheckCircle2, AlertTriangle, Clock } from "lucide-react";
import type { DailyBrief, AgentStatus, ApprovalRequest } from "@/lib/types";

const MOCK_BRIEF: DailyBrief = {
  brief_date: "2025-02-03",
  generated_at: "2025-02-03T06:00:00Z",
  top_threats: [
    {
      rank: 1,
      title: "Steel delivery delay risk from port congestion",
      agent_source: "supply_chain",
      impact: "$150K cost, 10-day schedule impact",
      confidence: 0.82,
      action_required: "Approve alternative vendor expedite",
    },
    {
      rank: 2,
      title: "Float erosion on critical path Zone A",
      agent_source: "schedule",
      impact: "3 days float consumed this week",
      confidence: 0.91,
      action_required: "Review crew reallocation plan",
    },
    {
      rank: 3,
      title: "Ironworker shortage next week",
      agent_source: "workforce",
      impact: "6-person gap, productivity at risk",
      confidence: 0.78,
      action_required: "Contact union hall for dispatch",
    },
  ],
  quality_gaps: [
    {
      rank: 1,
      title: "Wall thickness deviation at Grid A-3",
      agent_source: "compliance",
      severity: "major",
      location: "Level 2, Grid A-3",
    },
    {
      rank: 2,
      title: "Concrete strength below spec",
      agent_source: "compliance",
      severity: "minor",
      location: "Level 1, Foundation F-12",
    },
  ],
  acceleration: {
    title: "Weekend concrete pour for Zone B",
    agent_source: "schedule",
    potential_savings_days: 3,
    cost: 45000,
    description:
      "Running weekend shift for Zone B pour could recover 3 days of float",
  },
  full_text: "",
};

export default function DashboardPage() {
  const { data: brief } = useAgentData<DailyBrief>(briefsApi.daily);
  const { data: agents } = useAgentData<AgentStatus[]>(agentsApi.status);
  const { data: approvals } = useAgentData<ApprovalRequest[]>(
    approvalsApi.list,
  );

  const displayBrief = brief ?? MOCK_BRIEF;
  const runningAgents = agents?.filter((a) => a.status === "running").length ?? 0;
  const idleAgents = agents?.filter((a) => a.status === "idle").length ?? 13;
  const errorAgents = agents?.filter((a) => a.status === "error").length ?? 0;
  const pendingApprovals =
    approvals?.filter((a) => a.status === "pending").length ?? 1;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Project Dashboard</h1>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
            <Bot size={20} className="text-primary" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-800">
              Agents Running
            </p>
            <p className="text-xl font-bold text-primary">{runningAgents}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center">
            <Clock size={20} className="text-gray-500" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-800">Agents Idle</p>
            <p className="text-xl font-bold text-gray-600">{idleAgents}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-danger/10 flex items-center justify-center">
            <AlertTriangle size={20} className="text-danger" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-800">Agent Errors</p>
            <p className="text-xl font-bold text-danger">{errorAgents}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-warning/10 flex items-center justify-center">
            <CheckCircle2 size={20} className="text-warning" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-800">
              Pending Approvals
            </p>
            <p className="text-xl font-bold text-warning">{pendingApprovals}</p>
          </div>
        </div>
      </div>

      {/* Daily Brief */}
      <DailyBriefCard brief={displayBrief} />
    </div>
  );
}
