"use client";

import { AlertTriangle, TrendingUp, Search } from "lucide-react";
import type { DailyBrief } from "@/lib/types";

interface DailyBriefCardProps {
  brief: DailyBrief;
}

export function DailyBriefCard({ brief }: DailyBriefCardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800">
          Daily Brief - {brief.brief_date}
        </h2>
        <span className="text-xs text-gray-500">
          Generated {new Date(brief.generated_at).toLocaleTimeString()}
        </span>
      </div>

      {/* Top 3 Threats */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-danger flex items-center gap-2 mb-3">
          <AlertTriangle size={16} />
          Top Threats
        </h3>
        <div className="space-y-3">
          {brief.top_threats.map((threat) => (
            <div
              key={threat.rank}
              className="flex items-start gap-3 p-3 bg-red-50 rounded-lg"
            >
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-danger text-white text-xs flex items-center justify-center font-bold">
                {threat.rank}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  {threat.title}
                </p>
                <p className="text-xs text-gray-600 mt-0.5">{threat.impact}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs text-gray-500">
                    via {threat.agent_source}
                  </span>
                  <span className="text-xs px-1.5 py-0.5 bg-gray-100 rounded">
                    {Math.round(threat.confidence * 100)}% conf
                  </span>
                </div>
                <p className="text-xs text-primary font-medium mt-1">
                  Action: {threat.action_required}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quality Gaps */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-warning flex items-center gap-2 mb-3">
          <Search size={16} />
          Quality Gaps
        </h3>
        <div className="space-y-2">
          {brief.quality_gaps.map((gap) => (
            <div
              key={gap.rank}
              className="flex items-start gap-3 p-3 bg-amber-50 rounded-lg"
            >
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-warning text-white text-xs flex items-center justify-center font-bold">
                {gap.rank}
              </span>
              <div>
                <p className="text-sm font-medium text-gray-900">{gap.title}</p>
                <p className="text-xs text-gray-600">
                  {gap.severity} - {gap.location}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Acceleration Opportunity */}
      {brief.acceleration && (
        <div>
          <h3 className="text-sm font-medium text-success flex items-center gap-2 mb-3">
            <TrendingUp size={16} />
            Acceleration Opportunity
          </h3>
          <div className="p-3 bg-green-50 rounded-lg">
            <p className="text-sm font-medium text-gray-900">
              {brief.acceleration.title}
            </p>
            <p className="text-xs text-gray-600 mt-0.5">
              {brief.acceleration.description}
            </p>
            <div className="flex gap-4 mt-2">
              <span className="text-xs text-success font-medium">
                Save {brief.acceleration.potential_savings_days} days
              </span>
              <span className="text-xs text-gray-500">
                Cost: ${brief.acceleration.cost.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
