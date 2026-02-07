export function createWebSocket(onMessage: (data: unknown) => void) {
  const wsUrl =
    process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/dashboard";
  const ws = new WebSocket(wsUrl);

  ws.onmessage = (event) => {
    try {
      onMessage(JSON.parse(event.data));
    } catch {
      console.error("Failed to parse WebSocket message");
    }
  };

  ws.onerror = (error) => console.error("WebSocket error:", error);

  ws.onclose = () => {
    setTimeout(() => createWebSocket(onMessage), 5000);
  };

  return ws;
}
