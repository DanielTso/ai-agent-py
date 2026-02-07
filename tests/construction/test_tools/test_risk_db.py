"""Tests for the risk database tool."""

import json

from construction.tools.risk_db import RiskDatabase


def test_schema():
    """Tool schema has required fields."""
    tool = RiskDatabase()
    assert tool.name == "risk_database"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "risk_id" in props
    assert "filters" in props
    assert "data" in props
    assert props["action"]["enum"] == ["query", "create", "update"]
    assert schema["required"] == ["action", "project_id"]


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = RiskDatabase()
    fmt = tool.to_api_format()
    assert fmt["name"] == "risk_database"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_query_all_risks():
    """Query action returns all active risks."""
    tool = RiskDatabase()
    result = tool.execute(action="query", project_id="PRJ-001")
    data = json.loads(result)
    assert "risks" in data
    assert data["total"] == 3
    for risk in data["risks"]:
        assert risk["project_id"] == "PRJ-001"
        assert risk["status"] == "active"


def test_query_by_category():
    """Query can filter by category."""
    tool = RiskDatabase()
    result = tool.execute(
        action="query",
        project_id="PRJ-001",
        filters={"category": "weather"},
    )
    data = json.loads(result)
    assert data["total"] == 1
    assert data["risks"][0]["category"] == "weather"


def test_query_by_status():
    """Query can filter by status."""
    tool = RiskDatabase()
    result = tool.execute(
        action="query",
        project_id="PRJ-001",
        filters={"status": "mitigated"},
    )
    data = json.loads(result)
    assert data["total"] == 0


def test_create_risk():
    """Create action returns new risk with ID."""
    tool = RiskDatabase()
    result = tool.execute(
        action="create",
        project_id="PRJ-001",
        data={
            "category": "labor",
            "description": "Electrician shortage expected",
            "probability": 0.3,
            "impact_dollars": 150000,
        },
    )
    data = json.loads(result)
    assert data["status"] == "success"
    assert "created" in data
    assert data["created"]["project_id"] == "PRJ-001"
    assert data["created"]["category"] == "labor"
    assert "id" in data["created"]


def test_create_without_data():
    """Create action returns error when data is missing."""
    tool = RiskDatabase()
    result = tool.execute(
        action="create", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "data is required" in result


def test_update_risk():
    """Update action returns updated risk."""
    tool = RiskDatabase()
    result = tool.execute(
        action="update",
        project_id="PRJ-001",
        risk_id="RISK-001",
        data={"status": "mitigated", "probability": 0.05},
    )
    data = json.loads(result)
    assert data["status"] == "success"
    assert data["updated"]["id"] == "RISK-001"
    assert data["updated"]["status"] == "mitigated"


def test_update_without_risk_id():
    """Update action returns error when risk_id is missing."""
    tool = RiskDatabase()
    result = tool.execute(
        action="update",
        project_id="PRJ-001",
        data={"status": "mitigated"},
    )
    assert "Error" in result
    assert "risk_id is required" in result


def test_update_without_data():
    """Update action returns error when data is missing."""
    tool = RiskDatabase()
    result = tool.execute(
        action="update",
        project_id="PRJ-001",
        risk_id="RISK-001",
    )
    assert "Error" in result
    assert "data is required" in result


def test_unknown_action():
    """Unknown action returns error."""
    tool = RiskDatabase()
    result = tool.execute(
        action="delete", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "unknown action" in result
