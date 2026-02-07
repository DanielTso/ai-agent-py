"""Typed access to shared Redis state for construction agents."""

import json
from datetime import datetime

import redis.asyncio as redis

from construction.config import get_construction_settings


class SharedMemory:
    """Provides typed get/set access to shared Redis state."""

    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
        settings = get_construction_settings()
        self._dedup_ttl = settings.dedup_ttl_seconds

    # --- Agent status ---

    async def set_agent_status(self, agent_name: str, status: str) -> None:
        """Set the current status for an agent."""
        await self._redis.set(f"agent:{agent_name}:status", status)

    async def get_agent_status(self, agent_name: str) -> str | None:
        """Get the current status for an agent."""
        val = await self._redis.get(f"agent:{agent_name}:status")
        return val.decode() if val else None

    # --- Agent last run ---

    async def set_agent_last_run(self, agent_name: str, timestamp: str) -> None:
        """Record when an agent last ran."""
        await self._redis.set(f"agent:{agent_name}:last_run", timestamp)

    async def get_agent_last_run(self, agent_name: str) -> str | None:
        """Get when an agent last ran."""
        val = await self._redis.get(f"agent:{agent_name}:last_run")
        return val.decode() if val else None

    # --- Active risks (sorted set by score) ---

    async def add_active_risk(self, project_id: str, risk_id: str, score: float) -> None:
        """Add or update an active risk with its score."""
        await self._redis.zadd(f"project:{project_id}:active_risks", {risk_id: score})

    async def get_active_risks(self, project_id: str) -> list[tuple[str, float]]:
        """Get active risks sorted by score (highest first)."""
        results = await self._redis.zrevrangebyscore(
            f"project:{project_id}:active_risks",
            "+inf",
            "-inf",
            withscores=True,
        )
        return [
            (member.decode() if isinstance(member, bytes) else member, score)
            for member, score in results
        ]

    # --- Critical path ---

    async def set_critical_path(self, project_id: str, activity_ids: list[str]) -> None:
        """Store the critical path activity IDs."""
        await self._redis.set(
            f"project:{project_id}:critical_path",
            json.dumps(activity_ids),
        )

    async def get_critical_path(self, project_id: str) -> list[str]:
        """Get the critical path activity IDs."""
        val = await self._redis.get(f"project:{project_id}:critical_path")
        return json.loads(val) if val else []

    # --- Vendor alerts ---

    async def add_vendor_alert(self, project_id: str, alert: dict) -> None:
        """Add a vendor alert to the list."""
        await self._redis.rpush(
            f"project:{project_id}:vendor_alerts",
            json.dumps(alert, default=_json_default),
        )

    async def get_vendor_alerts(self, project_id: str) -> list[dict]:
        """Get all vendor alerts."""
        raw = await self._redis.lrange(f"project:{project_id}:vendor_alerts", 0, -1)
        return [json.loads(item) for item in raw]

    # --- Pending approvals ---

    async def add_pending_approval(self, project_id: str, approval_id: str) -> None:
        """Add a pending approval ID."""
        await self._redis.sadd(f"project:{project_id}:pending_approvals", approval_id)

    async def get_pending_approvals(self, project_id: str) -> list[str]:
        """Get all pending approval IDs."""
        members = await self._redis.smembers(f"project:{project_id}:pending_approvals")
        return [m.decode() if isinstance(m, bytes) else m for m in members]

    # --- Budget status ---

    async def set_budget_status(self, project_id: str, evm_snapshot: dict) -> None:
        """Store the current EVM budget snapshot."""
        await self._redis.set(
            f"project:{project_id}:budget_status",
            json.dumps(evm_snapshot, default=_json_default),
        )

    async def get_budget_status(self, project_id: str) -> dict | None:
        """Get the current EVM budget snapshot."""
        val = await self._redis.get(f"project:{project_id}:budget_status")
        return json.loads(val) if val else None

    # --- Labor availability ---

    async def set_labor_availability(self, project_id: str, data: dict) -> None:
        """Store labor availability data."""
        await self._redis.set(
            f"project:{project_id}:labor_availability",
            json.dumps(data, default=_json_default),
        )

    async def get_labor_availability(self, project_id: str) -> dict | None:
        """Get labor availability data."""
        val = await self._redis.get(f"project:{project_id}:labor_availability")
        return json.loads(val) if val else None

    # --- Commissioning status ---

    async def set_commissioning_status(self, project_id: str, data: dict) -> None:
        """Store commissioning status data."""
        await self._redis.set(
            f"project:{project_id}:commissioning_status",
            json.dumps(data, default=_json_default),
        )

    async def get_commissioning_status(self, project_id: str) -> dict | None:
        """Get commissioning status data."""
        val = await self._redis.get(f"project:{project_id}:commissioning_status")
        return json.loads(val) if val else None

    # --- Safety readiness ---

    async def set_safety_readiness(self, project_id: str, score: float) -> None:
        """Store the safety readiness score."""
        await self._redis.set(f"project:{project_id}:safety_readiness", str(score))

    async def get_safety_readiness(self, project_id: str) -> float | None:
        """Get the safety readiness score."""
        val = await self._redis.get(f"project:{project_id}:safety_readiness")
        return float(val) if val else None

    # --- TRIR ---

    async def set_trir_current(self, project_id: str, value: float) -> None:
        """Store the current TRIR value."""
        await self._redis.set(f"project:{project_id}:trir_current", str(value))

    async def get_trir_current(self, project_id: str) -> float | None:
        """Get the current TRIR value."""
        val = await self._redis.get(f"project:{project_id}:trir_current")
        return float(val) if val else None

    # --- Deduplication ---

    async def check_dedup(self, alert_hash: str) -> bool:
        """Return True if alert_hash has already been seen."""
        val = await self._redis.get(f"dedup:{alert_hash}")
        return val is not None

    async def mark_dedup(self, alert_hash: str) -> None:
        """Mark an alert_hash as seen with TTL."""
        await self._redis.set(f"dedup:{alert_hash}", "1", ex=self._dedup_ttl)


def _json_default(obj: object) -> str:
    """JSON serializer fallback for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
