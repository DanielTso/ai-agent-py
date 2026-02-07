"""FastAPI dependency injection."""

from construction.config import (
    ConstructionSettings,
    get_construction_settings,
)


async def get_settings() -> ConstructionSettings:
    return get_construction_settings()


async def get_project_id() -> str:
    """Default project ID for single-project deployments."""
    return "default-project"
