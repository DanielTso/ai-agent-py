"""Agent management API endpoints."""

from fastapi import APIRouter

router = APIRouter()

_AGENT_NAMES = [
    "risk_forecaster",
    "supply_chain",
    "critical_path",
    "compliance",
    "document_intelligence",
    "financial",
    "workforce",
    "communication",
    "commissioning",
    "environmental",
    "claims",
    "site_logistics",
    "safety",
]


@router.get("/status")
async def get_agent_statuses():
    """All agent statuses."""
    return [
        {
            "name": agent,
            "status": "idle",
            "last_run": "2025-02-03T06:00:00Z",
            "runs_today": 3,
            "avg_duration_seconds": 12.5,
            "errors_today": 0,
        }
        for agent in _AGENT_NAMES
    ]


@router.post("/{agent_name}/run")
async def trigger_agent_run(agent_name: str):
    """Trigger an agent run."""
    return {
        "agent_name": agent_name,
        "run_id": f"RUN-{agent_name}-001",
        "status": "started",
        "message": f"Agent {agent_name} run triggered",
    }


@router.get("/{agent_name}/history")
async def get_agent_history(agent_name: str):
    """Agent run history."""
    return [
        {
            "run_id": f"RUN-{agent_name}-003",
            "started_at": "2025-02-03T06:00:00Z",
            "completed_at": "2025-02-03T06:00:12Z",
            "status": "completed",
            "findings": 2,
            "approvals_created": 1,
        },
        {
            "run_id": f"RUN-{agent_name}-002",
            "started_at": "2025-02-02T06:00:00Z",
            "completed_at": "2025-02-02T06:00:15Z",
            "status": "completed",
            "findings": 0,
            "approvals_created": 0,
        },
    ]
