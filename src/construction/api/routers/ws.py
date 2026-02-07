"""WebSocket endpoint for real-time dashboard updates."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from construction.api.websocket import manager

router = APIRouter()


@router.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    """WebSocket endpoint for dashboard real-time updates."""
    await manager.connect(websocket)
    try:
        # Send initial state on connect
        await websocket.send_json(
            {
                "type": "connection_established",
                "message": "Connected to Construction PM AI",
            }
        )
        # Keep connection alive, relay events
        while True:
            data = await websocket.receive_text()
            # Echo back for now; will relay Redis pub/sub
            await websocket.send_json(
                {"type": "ack", "received": data}
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
