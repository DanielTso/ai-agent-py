"""Configuration management for the AI agent."""

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    model: str = Field(default="claude-sonnet-4-5-20250929", alias="MODEL")
    max_tokens: int = Field(default=4096, alias="MAX_TOKENS")

    model_config = {"env_file": ".env", "extra": "ignore"}


def get_settings() -> Settings:
    """Return application settings."""
    return Settings()
