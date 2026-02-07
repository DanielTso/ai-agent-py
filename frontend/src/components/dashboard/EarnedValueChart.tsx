"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { EarnedValue } from "@/lib/types";

interface EarnedValueChartProps {
  evm: EarnedValue;
}

export function EarnedValueChart({ evm }: EarnedValueChartProps) {
  // Build multi-period trend data from the single EVM snapshot
  // In production this would come from a time-series endpoint
  const data = [
    { month: "Oct", cpi: 1.02, spi: 1.01 },
    { month: "Nov", cpi: 0.99, spi: 0.98 },
    { month: "Dec", cpi: 0.97, spi: 0.97 },
    { month: "Jan", cpi: 0.95, spi: 0.95 },
    { month: "Feb", cpi: evm.cpi, spi: evm.spi },
  ];

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        CPI / SPI Trend
      </h2>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" tick={{ fontSize: 12 }} />
            <YAxis
              domain={[0.85, 1.15]}
              tick={{ fontSize: 12 }}
              tickFormatter={(v: number) => v.toFixed(2)}
            />
            <Tooltip
              formatter={(value: number) => value.toFixed(3)}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="cpi"
              name="CPI"
              stroke="#1e40af"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="spi"
              name="SPI"
              stroke="#16a34a"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
            {/* Target line at 1.0 */}
            <Line
              type="monotone"
              dataKey={() => 1.0}
              name="Target"
              stroke="#9ca3af"
              strokeWidth={1}
              strokeDasharray="5 5"
              dot={false}
              legendType="none"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-4 gap-4 mt-4 text-center">
        <div>
          <p className="text-xs text-gray-500">PV (BCWS)</p>
          <p className="text-sm font-bold">
            ${(evm.bcws / 1_000_000).toFixed(1)}M
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500">EV (BCWP)</p>
          <p className="text-sm font-bold">
            ${(evm.bcwp / 1_000_000).toFixed(1)}M
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500">AC (ACWP)</p>
          <p className="text-sm font-bold">
            ${(evm.acwp / 1_000_000).toFixed(1)}M
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500">EAC</p>
          <p className="text-sm font-bold">
            ${(evm.eac / 1_000_000).toFixed(1)}M
          </p>
        </div>
      </div>
    </div>
  );
}
