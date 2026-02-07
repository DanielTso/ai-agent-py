"use client";

import { Bot, Play, Loader2, AlertCircle } from "lucide-react";
import type { AgentStatus } from "@/lib/types";

interface AgentStatusPanelProps {
  agents: AgentStatus[];
  onTrigger?: (agentName: string) => void;
}

const STATUS_CONFIG: Record<string, { color: string; icon: typeof Bot }> = {
  idle: { color: "text-gray-500", icon: Bot },
  running: { color: "text-primary", icon: Loader2 },
  error: { color: "text-danger", icon: AlertCircle },
};

export function AgentStatusPanel({ agents, onTrigger }: AgentStatusPanelProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Agent Status
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {agents.map((agent) => {
          const config = STATUS_CONFIG[agent.status] ?? STATUS_CONFIG.idle;
          const Icon = config.icon;

          return (
            <div
              key={agent.name}
              className="flex items-center gap-3 p-3 border border-gray-100 rounded-lg hover:border-gray-200 transition-colors"
            >
              <div
                className={`w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center ${config.color}`}
              >
                <Icon
                  size={20}
                  className={agent.status === "running" ? "animate-spin" : ""}
                />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-800 truncate">
                  {agent.name.replace(/_/g, " ")}
                </p>
                <div className="flex items-center gap-2">
                  <span
                    className={`text-xs font-medium ${
                      agent.status === "running"
                        ? "text-primary"
                        : agent.status === "error"
                          ? "text-danger"
                          : "text-gray-500"
                    }`}
                  >
                    {agent.status}
                  </span>
                  <span className="text-xs text-gray-400">
                    {agent.runs_today} runs
                  </span>
                </div>
                <p className="text-xs text-gray-400">
                  Last: {new Date(agent.last_run).toLocaleTimeString()}
                </p>
              </div>
              {onTrigger && (
                <button
                  onClick={() => onTrigger(agent.name)}
                  className="p-1.5 rounded hover:bg-gray-100 transition-colors"
                  title={`Trigger ${agent.name}`}
                >
                  <Play size={14} className="text-gray-500" />
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
