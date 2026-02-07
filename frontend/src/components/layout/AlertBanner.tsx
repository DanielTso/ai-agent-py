"use client";

import { useState } from "react";
import { AlertTriangle, X } from "lucide-react";

interface AlertBannerProps {
  message: string;
  severity?: "warning" | "critical";
}

export function AlertBanner({
  message,
  severity = "warning",
}: AlertBannerProps) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return (
    <div
      className={`flex items-center justify-between px-4 py-2 text-sm ${
        severity === "critical"
          ? "bg-danger/10 text-danger border-b border-danger/20"
          : "bg-warning/10 text-amber-800 border-b border-warning/20"
      }`}
    >
      <div className="flex items-center gap-2">
        <AlertTriangle size={16} />
        <span>{message}</span>
      </div>
      <button
        onClick={() => setDismissed(true)}
        className="p-1 rounded hover:bg-black/5"
        aria-label="Dismiss alert"
      >
        <X size={14} />
      </button>
    </div>
  );
}
