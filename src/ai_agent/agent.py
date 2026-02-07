"""Core agent implementation."""

from anthropic import Anthropic

from ai_agent.config import Settings, get_settings
from ai_agent.tools import ToolRegistry


class Agent:
    """An AI agent that interacts with Claude via the Anthropic API."""

    def __init__(self, settings: Settings | None = None, tool_registry: ToolRegistry | None = None):
        self.settings = settings or get_settings()
        self.client = Anthropic(api_key=self.settings.anthropic_api_key)
        self.conversation: list[dict] = []
        self.tool_registry = tool_registry or ToolRegistry()

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the agent.

        Implements an agentic loop: if Claude requests tool use, the agent
        executes the tools, sends results back, and repeats until Claude
        produces a final text response.
        """
        self.conversation.append({"role": "user", "content": user_message})

        tools = self.tool_registry.to_api_format() if len(self.tool_registry) > 0 else None
        self.last_tool_calls: list[dict] = []

        while True:
            kwargs: dict = {
                "model": self.settings.model,
                "max_tokens": self.settings.max_tokens,
                "messages": self.conversation,
            }
            if tools:
                kwargs["tools"] = tools

            response = self.client.messages.create(**kwargs)

            # Store the full content blocks for multi-turn correctness
            self.conversation.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool = self.tool_registry.get(block.name)
                        if tool:
                            result = tool.execute(**block.input)
                        else:
                            result = f"Error: unknown tool '{block.name}'"
                        self.last_tool_calls.append({
                            "tool": block.name, "input": block.input, "result": result,
                        })
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })
                self.conversation.append({"role": "user", "content": tool_results})
            else:
                # End of turn — extract text from the final response
                text_parts = [block.text for block in response.content if block.type == "text"]
                return text_parts[0] if text_parts else ""

    def reset(self):
        """Clear conversation history."""
        self.conversation = []
