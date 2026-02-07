"""Core agent implementation."""

from anthropic import Anthropic

from ai_agent.config import Settings, get_settings


class Agent:
    """An AI agent that interacts with Claude via the Anthropic API."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.client = Anthropic(api_key=self.settings.anthropic_api_key)
        self.conversation: list[dict] = []

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the agent."""
        self.conversation.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=self.settings.model,
            max_tokens=self.settings.max_tokens,
            messages=self.conversation,
        )

        assistant_message = response.content[0].text
        self.conversation.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def reset(self):
        """Clear conversation history."""
        self.conversation = []
