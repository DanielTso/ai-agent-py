"use client";

import { useState, useEffect, useCallback, useRef } from "react";

interface UseAgentDataOptions {
  refreshInterval?: number;
}

export function useAgentData<T>(
  fetcher: () => Promise<T>,
  options?: UseAgentDataOptions,
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetcherRef = useRef(fetcher);
  fetcherRef.current = fetcher;

  const refresh = useCallback(async () => {
    try {
      setLoading(true);
      const result = await fetcherRef.current();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();

    if (options?.refreshInterval) {
      const interval = setInterval(refresh, options.refreshInterval);
      return () => clearInterval(interval);
    }
  }, [refresh, options?.refreshInterval]);

  return { data, loading, error, refresh };
}
