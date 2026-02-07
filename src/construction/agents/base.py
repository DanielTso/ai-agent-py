"""Base class for all construction PM agents."""

import uuid
from abc import ABC, abstractmethod
from datetime import UTC, datetime

from ai_agent.agent import Agent
from ai_agent.config import Settings
from ai_agent.tools import ToolRegistry
from construction.config import ConstructionSettings, get_construction_settings
from construction.redis_.pubsub import AgentPubSub
from construction.redis_.shared_memory import SharedMemory
from construction.schemas.common import AgentEvent, DataSource


class ConstructionAgent(ABC):
    """Base class for all 13 construction PM agents."""

    name: str  # e.g. "risk_forecaster"
    description: str
    schedule: str  # e.g. "hourly", "daily", "on_demand"

    def __init__(
        self,
        settings: ConstructionSettings | None = None,
        shared_memory: SharedMemory | None = None,
        pubsub: AgentPubSub | None = None,
    ):
        self.settings = settings or get_construction_settings()
        self.shared_memory = shared_memory
        self.pubsub = pubsub
        self._tools = ToolRegistry()
        self._register_tools()
        self._agent = Agent(
            settings=Settings(
                anthropic_api_key=self.settings.anthropic_api_key,
                model=self.settings.model,
                max_tokens=self.settings.max_tokens,
            ),
            tool_registry=self._tools,
            system_prompt=self.get_system_prompt(),
        )

    @abstractmethod
    def _register_tools(self) -> None:
        """Register tools specific to this agent."""

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent's persona."""

    @abstractmethod
    async def run(self, context: dict | None = None) -> AgentEvent:
        """Execute the agent's primary task. Returns an AgentEvent."""

    def chat(self, message: str) -> str:
        """Send a message to the underlying Claude agent."""
        return self._agent.chat(message)

    async def publish_event(
        self,
        event_type: str,
        severity: str,
        data: dict,
        confidence: float,
        data_sources: list[DataSource],
        transparency_log: list[str],
        requires_cross_agent: bool = False,
        target_agent: str | None = None,
    ) -> AgentEvent:
        """Publish an agent event to the pub/sub system."""
        event = AgentEvent(
            event_id=str(uuid.uuid4()),
            source_agent=self.name,
            event_type=event_type,
            severity=severity,
            timestamp=datetime.now(UTC),
            data=data,
            confidence=confidence,
            data_sources=data_sources,
            transparency_log=transparency_log,
            requires_cross_agent=requires_cross_agent,
            target_agent=target_agent,
        )
        if self.pubsub:
            await self.pubsub.publish("channel:agent_events", event.model_dump())
            if severity == "critical":
                await self.pubsub.publish("channel:escalation", event.model_dump())
        if self.shared_memory:
            await self.shared_memory.set_agent_status(self.name, "completed")
            await self.shared_memory.set_agent_last_run(self.name, datetime.now(UTC).isoformat())
        return event
