"use client";

import { useEffect, useRef, useCallback, useState } from "react";
import { createWebSocket } from "@/lib/websocket";

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const [lastMessage, setLastMessage] = useState<unknown>(null);
  const [connected, setConnected] = useState(false);

  const handleMessage = useCallback((data: unknown) => {
    setLastMessage(data);
  }, []);

  useEffect(() => {
    wsRef.current = createWebSocket(handleMessage);

    const ws = wsRef.current;
    const onOpen = () => setConnected(true);
    const onClose = () => setConnected(false);

    ws.addEventListener("open", onOpen);
    ws.addEventListener("close", onClose);

    return () => {
      ws.removeEventListener("open", onOpen);
      ws.removeEventListener("close", onClose);
      ws.close();
    };
  }, [handleMessage]);

  return { lastMessage, connected };
}
