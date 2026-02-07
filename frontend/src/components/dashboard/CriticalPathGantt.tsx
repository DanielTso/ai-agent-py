"use client";

import type { Activity } from "@/lib/types";

interface CriticalPathGanttProps {
  activities: Activity[];
  totalDurationDays: number;
}

export function CriticalPathGantt({
  activities,
  totalDurationDays,
}: CriticalPathGanttProps) {
  // Find the earliest start date to use as baseline
  const dates = activities
    .filter((a) => a.start_date && a.end_date)
    .map((a) => ({
      ...a,
      start: new Date(a.start_date!),
      end: new Date(a.end_date!),
    }));

  const minDate =
    dates.length > 0
      ? new Date(Math.min(...dates.map((d) => d.start.getTime())))
      : new Date();

  const maxDate =
    dates.length > 0
      ? new Date(Math.max(...dates.map((d) => d.end.getTime())))
      : new Date();

  const totalRange = maxDate.getTime() - minDate.getTime() || 1;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Critical Path</h2>
        <span className="text-sm text-gray-500">
          {totalDurationDays} days total
        </span>
      </div>

      <div className="space-y-3">
        {dates.map((activity) => {
          const leftPct =
            ((activity.start.getTime() - minDate.getTime()) / totalRange) * 100;
          const widthPct =
            ((activity.end.getTime() - activity.start.getTime()) / totalRange) *
            100;

          return (
            <div key={activity.id} className="flex items-center gap-3">
              <div className="w-48 flex-shrink-0">
                <p className="text-sm font-medium text-gray-800 truncate">
                  {activity.name}
                </p>
                <p className="text-xs text-gray-500">
                  {activity.start_date} - {activity.end_date}
                </p>
              </div>
              <div className="flex-1 bg-gray-100 rounded-full h-6 relative">
                <div
                  className={`absolute h-6 rounded-full flex items-center px-2 text-xs text-white font-medium ${
                    activity.is_critical ? "bg-danger" : "bg-primary-light"
                  }`}
                  style={{
                    left: `${leftPct}%`,
                    width: `${Math.max(widthPct, 5)}%`,
                  }}
                >
                  {activity.external_id}
                </div>
              </div>
              <div className="w-20 text-right flex-shrink-0">
                <span
                  className={`text-xs font-medium px-2 py-1 rounded ${
                    activity.total_float === 0
                      ? "bg-red-100 text-danger"
                      : activity.total_float <= 5
                        ? "bg-amber-100 text-amber-700"
                        : "bg-green-100 text-success"
                  }`}
                >
                  {activity.total_float}d float
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
