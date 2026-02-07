"use client";

import { FinancialSummary } from "@/components/dashboard/FinancialSummary";
import { EarnedValueChart } from "@/components/dashboard/EarnedValueChart";
import { useAgentData } from "@/hooks/useAgentData";
import { financialApi } from "@/lib/api";
import type { BudgetStatus, EarnedValue, ChangeOrder } from "@/lib/types";

const MOCK_BUDGET: BudgetStatus = {
  project_id: "default-project",
  total_budget: 20000000,
  spent_to_date: 5100000,
  committed: 8500000,
  forecast_at_completion: 21276596,
  contingency_remaining: 1200000,
  variance_pct: -0.064,
};

const MOCK_EVM: EarnedValue = {
  snapshot_date: "2025-02-01",
  bcws: 5000000,
  bcwp: 4800000,
  acwp: 5100000,
  cpi: 0.94,
  spi: 0.96,
  eac: 21276596,
  etc: 16176596,
  vac: -1276596,
  tcpi: 1.04,
};

const MOCK_COS: ChangeOrder[] = [
  {
    id: "CO-001",
    co_number: "CO-2025-001",
    description: "Additional foundation work due to unforeseen soil conditions",
    cost_impact: 350000,
    schedule_impact_days: 7,
    status: "approved",
    submitted_date: "2025-01-20",
    approved_date: "2025-01-28",
  },
  {
    id: "CO-002",
    co_number: "CO-2025-002",
    description: "Owner-requested lobby upgrade",
    cost_impact: 180000,
    schedule_impact_days: 0,
    status: "pending",
    submitted_date: "2025-02-05",
    approved_date: null,
  },
];

export default function FinancialPage() {
  const { data: budget } = useAgentData<BudgetStatus>(financialApi.budget);
  const { data: evm } = useAgentData<EarnedValue>(financialApi.evm);
  const { data: changeOrders } = useAgentData<ChangeOrder[]>(
    financialApi.changeOrders,
  );

  const displayBudget = budget ?? MOCK_BUDGET;
  const displayEvm = evm ?? MOCK_EVM;
  const displayCOs = changeOrders ?? MOCK_COS;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">
        Financial Dashboard
      </h1>

      <FinancialSummary budget={displayBudget} evm={displayEvm} />
      <EarnedValueChart evm={displayEvm} />

      {/* Change Orders */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Change Orders
        </h2>
        <div className="space-y-3">
          {displayCOs.map((co) => (
            <div
              key={co.id}
              className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-mono text-gray-500">
                    {co.co_number}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      co.status === "approved"
                        ? "bg-green-100 text-success"
                        : co.status === "pending"
                          ? "bg-amber-100 text-amber-700"
                          : "bg-red-100 text-danger"
                    }`}
                  >
                    {co.status}
                  </span>
                </div>
                <p className="text-sm text-gray-800">{co.description}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold text-gray-800">
                  ${co.cost_impact.toLocaleString()}
                </p>
                {co.schedule_impact_days > 0 && (
                  <p className="text-xs text-danger">
                    +{co.schedule_impact_days}d
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
