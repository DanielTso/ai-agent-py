"use client";

import { VendorStatusTable } from "@/components/dashboard/VendorStatusTable";
import { useAgentData } from "@/hooks/useAgentData";
import { supplyChainApi } from "@/lib/api";
import { AlertTriangle } from "lucide-react";
import type { VendorStatus, SupplyChainAlert } from "@/lib/types";

const MOCK_VENDORS: VendorStatus[] = [
  {
    id: "V-001",
    name: "Acme Steel Corp",
    material: "Structural Steel W14x90",
    lead_time_days: 45,
    current_status: "on_track",
    port_of_origin: "Busan, South Korea",
    last_updated: "2025-02-01T00:00:00Z",
  },
  {
    id: "V-002",
    name: "BuildRight Concrete",
    material: "Ready-Mix 5000 PSI",
    lead_time_days: 3,
    current_status: "on_track",
    port_of_origin: null,
    last_updated: "2025-02-01T00:00:00Z",
  },
];

const MOCK_ALERTS: SupplyChainAlert[] = [
  {
    vendor_id: "V-003",
    shipment_id: "SHIP-003",
    alert_type: "delay",
    severity: "warning",
    description:
      "Curtain wall panels delayed 10 days due to port congestion",
    alternatives: [
      {
        alt_vendor: "GlassTech Inc",
        cost_delta: 15000,
        schedule_delta_days: -5,
        recommended: true,
        notes: null,
        confidence: 0.78,
      },
    ],
  },
];

export default function SupplyChainPage() {
  const { data: vendors } = useAgentData<VendorStatus[]>(
    supplyChainApi.vendors,
  );
  const { data: alerts } = useAgentData<SupplyChainAlert[]>(
    supplyChainApi.alerts,
  );

  const displayVendors = vendors ?? MOCK_VENDORS;
  const displayAlerts = alerts ?? MOCK_ALERTS;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Supply Chain Dashboard
      </h1>

      {/* Alerts */}
      {displayAlerts.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <AlertTriangle size={18} className="text-warning" />
            Active Alerts
          </h2>
          <div className="space-y-3">
            {displayAlerts.map((alert, idx) => (
              <div key={idx} className="p-4 bg-amber-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      alert.severity === "critical"
                        ? "bg-red-100 text-danger"
                        : "bg-amber-200 text-amber-800"
                    }`}
                  >
                    {alert.severity}
                  </span>
                  <span className="text-xs text-gray-500">
                    {alert.alert_type}
                  </span>
                </div>
                <p className="text-sm text-gray-800">{alert.description}</p>
                {alert.alternatives.length > 0 && (
                  <div className="mt-2 pl-3 border-l-2 border-amber-300">
                    <p className="text-xs text-gray-500 font-medium mb-1">
                      Alternatives:
                    </p>
                    {alert.alternatives.map((alt, i) => (
                      <div key={i} className="text-xs text-gray-600">
                        {alt.alt_vendor} - Cost delta: $
                        {alt.cost_delta.toLocaleString()}, Schedule:{" "}
                        {alt.schedule_delta_days}d
                        {alt.recommended && (
                          <span className="ml-1 text-success font-medium">
                            (Recommended)
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <VendorStatusTable vendors={displayVendors} />
    </div>
  );
}
