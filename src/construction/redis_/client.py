"""Redis connection pool management."""

import redis.asyncio as redis

from construction.config import get_construction_settings

_pool: redis.ConnectionPool | None = None


async def get_redis_pool() -> redis.ConnectionPool:
    """Return or create the shared Redis connection pool."""
    global _pool
    if _pool is None:
        settings = get_construction_settings()
        _pool = redis.ConnectionPool.from_url(settings.redis_url)
    return _pool


async def get_redis_client() -> redis.Redis:
    """Return a Redis client using the shared connection pool."""
    pool = await get_redis_pool()
    return redis.Redis(connection_pool=pool)


async def close_redis_pool():
    """Disconnect and discard the shared connection pool."""
    global _pool
    if _pool is not None:
        await _pool.disconnect()
        _pool = None
