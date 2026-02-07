"""Construction PM settings via pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class ConstructionSettings(BaseSettings):
    """All configuration for the Construction PM ecosystem."""

    model_config = {"env_file": ".env", "extra": "ignore"}

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/construction_pm"
    db_echo: bool = False

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Anthropic
    anthropic_api_key: str = ""
    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 8192

    # Project defaults
    project_name: str = ""
    project_tier: str = "III"
    contract_value: float = 0.0
    penalty_per_day: float = 500000.0

    # Risk thresholds
    risk_probability_threshold: float = 0.15
    risk_impact_threshold: float = 100000.0
    budget_variance_threshold: float = 0.10
    float_consumed_threshold: float = 0.80
    confidence_threshold: float = 0.70
    escalation_impact_threshold: float = 250000.0

    # External API keys
    openweathermap_api_key: str = ""
    procore_client_id: str = ""
    procore_client_secret: str = ""
    autodesk_client_id: str = ""
    autodesk_client_secret: str = ""
    primavera_api_url: str = ""
    primavera_api_key: str = ""
    ms_project_api_url: str = ""
    ms_project_api_key: str = ""
    portcast_api_key: str = ""
    vizion_api_key: str = ""
    terminal49_api_key: str = ""

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""
    pm_phone_number: str = ""

    # Regulatory API keys
    nfpa_api_key: str = ""
    epa_echo_api_key: str = ""
    icc_api_key: str = ""
    uptime_api_key: str = ""

    # Alert dedup
    dedup_ttl_seconds: int = 14400


@lru_cache
def get_construction_settings() -> ConstructionSettings:
    """Return cached construction settings singleton."""
    return ConstructionSettings()
