"""Redis pub/sub for inter-agent communication."""

import asyncio
import hashlib
import json
from collections.abc import Callable
from datetime import datetime

import redis.asyncio as redis

from construction.config import get_construction_settings

# Standard channels
AGENT_EVENTS = "channel:agent_events"
ESCALATION = "channel:escalation"
APPROVAL_UPDATES = "channel:approval_updates"
DASHBOARD_UPDATES = "channel:dashboard_updates"
FINANCIAL_UPDATES = "channel:financial_updates"
WORKFORCE_UPDATES = "channel:workforce_updates"
COMMISSIONING_UPDATES = "channel:commissioning_updates"
SITE_LOGISTICS = "channel:site_logistics"
SAFETY_ALERTS = "channel:safety_alerts"


class AgentPubSub:
    """Manages Redis pub/sub for inter-agent communication."""

    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
        self._pubsub = redis_client.pubsub()
        self._callbacks: dict[str, list[Callable]] = {}
        self._listener_task: asyncio.Task | None = None
        self._running = False
        settings = get_construction_settings()
        self._dedup_ttl = settings.dedup_ttl_seconds

    async def publish(self, channel: str, message_dict: dict) -> None:
        """Publish a message to a channel with deduplication."""
        payload = json.dumps(message_dict, default=_json_default)
        msg_hash = hashlib.sha256(payload.encode()).hexdigest()

        # Check dedup
        dedup_key = f"dedup:pubsub:{msg_hash}"
        already_seen = await self._redis.get(dedup_key)
        if already_seen:
            return

        await self._redis.set(dedup_key, "1", ex=self._dedup_ttl)
        await self._redis.publish(channel, payload)

    async def subscribe(self, channel: str, callback: Callable) -> None:
        """Subscribe to a channel with a callback."""
        if channel not in self._callbacks:
            self._callbacks[channel] = []
            await self._pubsub.subscribe(channel)
        self._callbacks[channel].append(callback)

    async def start_listening(self) -> None:
        """Start the background listener task."""
        self._running = True
        self._listener_task = asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        """Listen for messages and dispatch to callbacks."""
        while self._running:
            try:
                message = await self._pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message and message["type"] == "message":
                    channel = message["channel"]
                    if isinstance(channel, bytes):
                        channel = channel.decode()
                    data = json.loads(message["data"])
                    for cb in self._callbacks.get(channel, []):
                        await cb(data)
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(1)

    async def stop(self) -> None:
        """Stop the listener and unsubscribe."""
        self._running = False
        if self._listener_task and not self._listener_task.done():
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
        await self._pubsub.unsubscribe()


def _json_default(obj: object) -> str:
    """JSON serializer fallback for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
