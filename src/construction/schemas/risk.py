"""Pydantic models for risk assessment and forecasting."""

from datetime import datetime

from pydantic import BaseModel, Field

from construction.schemas.common import DataSource


class RiskScore(BaseModel):
    """Quantified risk scoring."""

    probability: float = Field(ge=0, le=1)
    impact_dollars: float = Field(ge=0)
    impact_days: float = Field(ge=0)
    safety_critical: bool = False
    composite_score: float = Field(
        ge=0,
        description="probability * impact_dollars",
    )


class RiskEvent(BaseModel):
    """A single identified risk event."""

    id: str
    project_id: str
    category: str  # weather/supply/labor/safety/environmental/financial
    description: str
    risk_score: RiskScore
    confidence: float = Field(ge=0, le=1)
    data_sources: list[DataSource] = []
    transparency_log: list[str] = []
    status: str = "active"
    created_at: datetime
    updated_at: datetime | None = None


class RiskHeatMapCell(BaseModel):
    """A single cell in the risk heat map."""

    probability_range: str
    impact_range: str
    count: int
    risk_ids: list[str] = []


class RiskHeatMap(BaseModel):
    """Risk heat map grid."""

    cells: list[RiskHeatMapCell] = []


class RiskAssessmentRequest(BaseModel):
    """Request for a risk assessment run."""

    project_id: str
    categories: list[str] | None = None
    timeframe_days: int = 14


class RiskAssessmentResponse(BaseModel):
    """Full risk assessment output."""

    risks: list[RiskEvent] = []
    heatmap: RiskHeatMap = RiskHeatMap()
    generated_at: datetime
    confidence: float = Field(ge=0, le=1)
