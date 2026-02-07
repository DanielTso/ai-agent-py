"use client";

import { AgentStatusPanel } from "@/components/dashboard/AgentStatusPanel";
import { useAgentData } from "@/hooks/useAgentData";
import { agentsApi } from "@/lib/api";
import type { AgentStatus } from "@/lib/types";

const AGENT_NAMES = [
  "risk_forecaster",
  "supply_chain",
  "critical_path",
  "compliance",
  "document_intelligence",
  "financial",
  "workforce",
  "communication",
  "commissioning",
  "environmental",
  "claims",
  "site_logistics",
  "safety",
];

const MOCK_AGENTS: AgentStatus[] = AGENT_NAMES.map((name) => ({
  name,
  status: "idle" as const,
  last_run: "2025-02-03T06:00:00Z",
  runs_today: 3,
  avg_duration_seconds: 12.5,
  errors_today: 0,
}));

export default function AgentsPage() {
  const { data: agents, refresh } = useAgentData<AgentStatus[]>(
    agentsApi.status,
    { refreshInterval: 10000 },
  );

  const displayAgents = agents ?? MOCK_AGENTS;

  const handleTrigger = async (agentName: string) => {
    try {
      await agentsApi.trigger(agentName);
      await refresh();
    } catch {
      // Error already handled by API layer
    }
  };

  const running = displayAgents.filter((a) => a.status === "running").length;
  const idle = displayAgents.filter((a) => a.status === "idle").length;
  const errors = displayAgents.filter((a) => a.status === "error").length;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Agent Monitoring</h1>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <p className="text-2xl font-bold text-primary">{running}</p>
          <p className="text-sm text-gray-500">Running</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <p className="text-2xl font-bold text-gray-600">{idle}</p>
          <p className="text-sm text-gray-500">Idle</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <p className="text-2xl font-bold text-danger">{errors}</p>
          <p className="text-sm text-gray-500">Errors</p>
        </div>
      </div>

      <AgentStatusPanel agents={displayAgents} onTrigger={handleTrigger} />
    </div>
  );
}
