"use client";

import { DollarSign, TrendingDown, TrendingUp } from "lucide-react";
import type { BudgetStatus, EarnedValue } from "@/lib/types";

interface FinancialSummaryProps {
  budget: BudgetStatus;
  evm: EarnedValue;
}

function formatCurrency(value: number): string {
  if (Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(1)}M`;
  }
  if (Math.abs(value) >= 1_000) {
    return `$${(value / 1_000).toFixed(0)}K`;
  }
  return `$${value.toFixed(0)}`;
}

export function FinancialSummary({ budget, evm }: FinancialSummaryProps) {
  const cards = [
    {
      label: "Total Budget",
      value: formatCurrency(budget.total_budget),
      sub: `Spent: ${formatCurrency(budget.spent_to_date)}`,
    },
    {
      label: "Forecast at Completion",
      value: formatCurrency(budget.forecast_at_completion),
      sub: `Variance: ${(budget.variance_pct * 100).toFixed(1)}%`,
      trend: budget.variance_pct < 0 ? "down" : "up",
    },
    {
      label: "Contingency Remaining",
      value: formatCurrency(budget.contingency_remaining),
      sub: `${((budget.contingency_remaining / budget.total_budget) * 100).toFixed(1)}% of budget`,
    },
    {
      label: "CPI / SPI",
      value: `${evm.cpi.toFixed(2)} / ${evm.spi.toFixed(2)}`,
      sub: `TCPI: ${evm.tcpi.toFixed(2)}`,
      trend: evm.cpi >= 1.0 ? "up" : "down",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="bg-white rounded-lg border border-gray-200 p-4"
        >
          <div className="flex items-center gap-2 mb-2">
            <DollarSign size={16} className="text-gray-400" />
            <span className="text-xs text-gray-500 font-medium">
              {card.label}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold text-gray-900">{card.value}</span>
            {card.trend === "up" && (
              <TrendingUp size={16} className="text-success" />
            )}
            {card.trend === "down" && (
              <TrendingDown size={16} className="text-danger" />
            )}
          </div>
          <p className="text-xs text-gray-500 mt-1">{card.sub}</p>
        </div>
      ))}
    </div>
  );
}
