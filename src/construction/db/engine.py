"""Async SQLAlchemy engine and session factory."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from construction.config import get_construction_settings


def get_engine():
    """Create an async engine from settings."""
    settings = get_construction_settings()
    return create_async_engine(settings.database_url, echo=settings.db_echo)


def get_session_factory(engine=None):
    """Create an async session factory, optionally reusing an existing engine."""
    if engine is None:
        engine = get_engine()
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
