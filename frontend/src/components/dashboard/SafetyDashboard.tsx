"use client";

import type { SafetyMetrics, ContractorSafetyProfile } from "@/lib/types";

interface SafetyDashboardProps {
  metrics: SafetyMetrics;
  contractors: ContractorSafetyProfile[];
  readinessScore?: number;
}

function GaugeCard({
  label,
  value,
  max,
  unit,
  thresholds,
}: {
  label: string;
  value: number;
  max: number;
  unit: string;
  thresholds: { good: number; warn: number };
}) {
  const pct = Math.min((value / max) * 100, 100);
  const color =
    value <= thresholds.good
      ? "text-success"
      : value <= thresholds.warn
        ? "text-warning"
        : "text-danger";
  const barColor =
    value <= thresholds.good
      ? "bg-success"
      : value <= thresholds.warn
        ? "bg-warning"
        : "bg-danger";

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <p className="text-xs text-gray-500 font-medium">{label}</p>
      <p className={`text-2xl font-bold mt-1 ${color}`}>
        {value.toFixed(2)}
        <span className="text-xs text-gray-400 ml-1">{unit}</span>
      </p>
      <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
        <div
          className={`h-2 rounded-full transition-all ${barColor}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export function SafetyDashboard({
  metrics,
  contractors,
  readinessScore,
}: SafetyDashboardProps) {
  return (
    <div className="space-y-6">
      {/* Safety Gauges */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Safety Metrics
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <GaugeCard
            label="TRIR"
            value={metrics.trir}
            max={5}
            unit=""
            thresholds={{ good: 2.0, warn: 3.5 }}
          />
          <GaugeCard
            label="DART"
            value={metrics.dart}
            max={3}
            unit=""
            thresholds={{ good: 1.0, warn: 2.0 }}
          />
          <GaugeCard
            label="EMR"
            value={metrics.emr}
            max={2}
            unit=""
            thresholds={{ good: 0.9, warn: 1.1 }}
          />
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 font-medium">
              Days Since Recordable
            </p>
            <p className="text-2xl font-bold mt-1 text-primary">
              {metrics.days_since_recordable}
            </p>
            <p className="text-xs text-gray-400 mt-2">
              {metrics.near_misses_ytd} near misses YTD
            </p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-4 text-center">
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-500">Recordables YTD</p>
            <p className="text-lg font-bold text-danger">
              {metrics.recordables_ytd}
            </p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-500">First Aid YTD</p>
            <p className="text-lg font-bold text-warning">
              {metrics.first_aid_ytd}
            </p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-500">Man-Hours YTD</p>
            <p className="text-lg font-bold text-gray-700">
              {(metrics.man_hours_ytd / 1000).toFixed(0)}K
            </p>
          </div>
        </div>
      </div>

      {/* Inspection Readiness */}
      {readinessScore !== undefined && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">
            Inspection Readiness
          </h2>
          <div className="flex items-center gap-4">
            <div
              className={`text-3xl font-bold ${
                readinessScore >= 85
                  ? "text-success"
                  : readinessScore >= 70
                    ? "text-warning"
                    : "text-danger"
              }`}
            >
              {readinessScore}%
            </div>
            <div className="flex-1 bg-gray-200 rounded-full h-4">
              <div
                className={`h-4 rounded-full ${
                  readinessScore >= 85
                    ? "bg-success"
                    : readinessScore >= 70
                      ? "bg-warning"
                      : "bg-danger"
                }`}
                style={{ width: `${readinessScore}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Contractor Safety Profiles */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Contractor Safety Profiles
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {contractors.map((c) => (
            <div
              key={c.contractor}
              className="p-4 border border-gray-100 rounded-lg"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-gray-800">
                  {c.contractor}
                </h3>
                <span
                  className={`text-xs px-2 py-0.5 rounded font-medium ${
                    c.prequalified
                      ? "bg-green-100 text-success"
                      : "bg-red-100 text-danger"
                  }`}
                >
                  {c.prequalified ? "Prequalified" : "Not Prequalified"}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div>
                  <p className="text-xs text-gray-500">EMR</p>
                  <p className="text-sm font-bold">{c.emr.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">TRIR</p>
                  <p className="text-sm font-bold">{c.trir.toFixed(1)}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Training</p>
                  <p className="text-sm font-bold">{c.training_compliance_pct}%</p>
                </div>
              </div>
              {c.incidents_ytd > 0 && (
                <p className="text-xs text-danger mt-2">
                  {c.incidents_ytd} incident(s) YTD
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
