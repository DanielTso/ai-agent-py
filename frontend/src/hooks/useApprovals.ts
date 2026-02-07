"use client";

import { useState, useEffect, useCallback } from "react";
import { approvalsApi } from "@/lib/api";
import type { ApprovalRequest } from "@/lib/types";

export function useApprovals() {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setLoading(true);
      const data = await approvalsApi.list();
      setApprovals(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load approvals");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const approve = useCallback(
    async (id: string, notes: string) => {
      await approvalsApi.approve(id, notes);
      await refresh();
    },
    [refresh],
  );

  const reject = useCallback(
    async (id: string, notes: string) => {
      await approvalsApi.reject(id, notes);
      await refresh();
    },
    [refresh],
  );

  return { approvals, loading, error, approve, reject, refresh };
}
