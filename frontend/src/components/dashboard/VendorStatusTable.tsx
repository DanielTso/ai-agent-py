"use client";

import type { VendorStatus } from "@/lib/types";

interface VendorStatusTableProps {
  vendors: VendorStatus[];
}

const STATUS_COLORS: Record<string, string> = {
  on_track: "bg-green-100 text-success",
  delayed: "bg-red-100 text-danger",
  at_risk: "bg-amber-100 text-amber-700",
  critical: "bg-red-200 text-red-800",
};

export function VendorStatusTable({ vendors }: VendorStatusTableProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Vendor Status
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Vendor
              </th>
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Material
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Lead Time
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Status
              </th>
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Origin
              </th>
            </tr>
          </thead>
          <tbody>
            {vendors.map((vendor) => (
              <tr
                key={vendor.id}
                className="border-b border-gray-100 hover:bg-gray-50"
              >
                <td className="py-2 px-3 font-medium text-gray-800">
                  {vendor.name}
                </td>
                <td className="py-2 px-3 text-gray-600">{vendor.material}</td>
                <td className="py-2 px-3 text-center text-gray-600">
                  {vendor.lead_time_days}d
                </td>
                <td className="py-2 px-3 text-center">
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${STATUS_COLORS[vendor.current_status] ?? "bg-gray-100 text-gray-600"}`}
                  >
                    {vendor.current_status.replace("_", " ")}
                  </span>
                </td>
                <td className="py-2 px-3 text-gray-600">
                  {vendor.port_of_origin ?? "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
