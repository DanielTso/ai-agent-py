"use client";

import type { RiskHeatMapCell } from "@/lib/types";

const PROB_LABELS = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"];
const IMPACT_LABELS = ["<$100k", "$100k-$250k", "$250k-$500k", "$500k-$1M", ">$1M"];

function getCellColor(count: number): string {
  if (count === 0) return "bg-gray-50";
  if (count === 1) return "bg-yellow-200";
  if (count === 2) return "bg-orange-300";
  if (count <= 4) return "bg-red-400";
  return "bg-red-600";
}

interface RiskHeatMapProps {
  cells: RiskHeatMapCell[];
}

export function RiskHeatMap({ cells }: RiskHeatMapProps) {
  // Build a lookup grid from the cells data
  const grid: number[][] = Array.from({ length: 5 }, () => Array(5).fill(0));

  cells.forEach((cell) => {
    const pIdx = PROB_LABELS.findIndex((l) =>
      cell.probability_range.includes(l.split("-")[0]),
    );
    const iIdx = IMPACT_LABELS.findIndex((l) =>
      cell.impact_range.includes(l.replace("$", "").split("-")[0]),
    );
    if (pIdx >= 0 && iIdx >= 0) {
      grid[4 - pIdx][iIdx] = cell.count;
    }
  });

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Risk Heat Map
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="w-24 p-2 text-xs text-gray-500 text-right">
                Probability
              </th>
              {IMPACT_LABELS.map((label) => (
                <th
                  key={label}
                  className="p-2 text-xs text-gray-500 font-medium text-center"
                >
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[...PROB_LABELS].reverse().map((probLabel, rowIdx) => (
              <tr key={probLabel}>
                <td className="p-2 text-xs text-gray-500 text-right font-medium">
                  {probLabel}
                </td>
                {grid[rowIdx].map((count, colIdx) => (
                  <td key={colIdx} className="p-1">
                    <div
                      className={`w-full h-12 rounded flex items-center justify-center text-sm font-bold ${getCellColor(count)} ${
                        count > 2 ? "text-white" : "text-gray-700"
                      }`}
                    >
                      {count > 0 ? count : ""}
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td />
              <td
                colSpan={5}
                className="text-center text-xs text-gray-500 pt-2"
              >
                Impact (Cost)
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
}
