"use client";

import type { OSHA300Record } from "@/lib/types";

interface OSHA300TableProps {
  records: OSHA300Record[];
}

export function OSHA300Table({ records }: OSHA300TableProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        OSHA 300 Log
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Case #
              </th>
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Employee
              </th>
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Date
              </th>
              <th className="text-left py-2 px-3 text-gray-500 font-medium">
                Description
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Classification
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Days Away
              </th>
              <th className="text-center py-2 px-3 text-gray-500 font-medium">
                Days Restricted
              </th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr
                key={record.case_number}
                className="border-b border-gray-100 hover:bg-gray-50"
              >
                <td className="py-2 px-3 font-mono text-xs">
                  {record.case_number}
                </td>
                <td className="py-2 px-3">{record.employee}</td>
                <td className="py-2 px-3 text-gray-600">
                  {record.date_of_injury}
                </td>
                <td className="py-2 px-3 text-gray-600 max-w-xs truncate">
                  {record.description}
                </td>
                <td className="py-2 px-3 text-center">
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      record.classification === "recordable"
                        ? "bg-red-100 text-danger"
                        : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {record.classification}
                  </span>
                </td>
                <td className="py-2 px-3 text-center">
                  {record.days_away > 0 ? (
                    <span className="text-danger font-medium">
                      {record.days_away}
                    </span>
                  ) : (
                    <span className="text-gray-400">0</span>
                  )}
                </td>
                <td className="py-2 px-3 text-center">
                  {record.days_restricted > 0 ? (
                    <span className="text-warning font-medium">
                      {record.days_restricted}
                    </span>
                  ) : (
                    <span className="text-gray-400">0</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
