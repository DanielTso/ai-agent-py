"""Tests for the workforce query tool."""

import json

from construction.tools.workforce import WorkforceQuery


def test_schema():
    """Tool schema has required fields."""
    tool = WorkforceQuery()
    assert tool.name == "workforce_query"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "trade" in props
    assert "worker_id" in props
    assert props["action"]["enum"] == [
        "crew_status",
        "productivity",
        "certifications",
        "labor_forecast",
    ]
    assert schema["required"] == ["action", "project_id"]


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = WorkforceQuery()
    fmt = tool.to_api_format()
    assert fmt["name"] == "workforce_query"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_crew_status_all():
    """crew_status returns all crews."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="crew_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "crews" in data
    assert len(data["crews"]) == 4


def test_crew_status_by_trade():
    """crew_status filters by trade."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="crew_status",
        project_id="PRJ-001",
        trade="electrical",
    )
    data = json.loads(result)
    assert len(data["crews"]) == 1
    assert data["crews"][0]["trade"] == "electrical"


def test_crew_status_structure():
    """crew_status returns expected fields."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="crew_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    crew = data["crews"][0]
    assert "trade" in crew
    assert "headcount" in crew
    assert "planned_production" in crew
    assert "actual_production" in crew
    assert "productivity_pct" in crew
    assert "location" in crew
    assert "overtime_hours" in crew


def test_productivity_all():
    """productivity returns all trades."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="productivity", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "productivity" in data
    assert len(data["productivity"]) == 4


def test_productivity_by_trade():
    """productivity filters by trade."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="productivity",
        project_id="PRJ-001",
        trade="mechanical",
    )
    data = json.loads(result)
    assert len(data["productivity"]) == 1
    assert data["productivity"][0]["trade"] == "mechanical"
    assert data["productivity"][0]["trend"] == "improving"


def test_productivity_structure():
    """productivity returns expected fields."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="productivity", project_id="PRJ-001"
    )
    data = json.loads(result)
    metric = data["productivity"][0]
    assert "trade" in metric
    assert "period" in metric
    assert "planned_units" in metric
    assert "actual_units" in metric
    assert "productivity_index" in metric
    assert "trend" in metric


def test_certifications_all():
    """certifications returns all workers."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="certifications", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "certifications" in data
    assert len(data["certifications"]) == 4


def test_certifications_by_worker():
    """certifications filters by worker_id."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="certifications",
        project_id="PRJ-001",
        worker_id="WRK-101",
    )
    data = json.loads(result)
    assert len(data["certifications"]) == 1
    assert data["certifications"][0]["worker_id"] == "WRK-101"
    assert data["certifications"][0]["status"] == "expiring_soon"


def test_certifications_structure():
    """certifications returns expected fields."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="certifications", project_id="PRJ-001"
    )
    data = json.loads(result)
    cert = data["certifications"][0]
    assert "worker_id" in cert
    assert "worker_name" in cert
    assert "cert_type" in cert
    assert "issue_date" in cert
    assert "expiry_date" in cert
    assert "status" in cert


def test_labor_forecast_all():
    """labor_forecast returns all trades."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="labor_forecast", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "labor_forecast" in data
    assert len(data["labor_forecast"]) == 4


def test_labor_forecast_by_trade():
    """labor_forecast filters by trade."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="labor_forecast",
        project_id="PRJ-001",
        trade="electrical",
    )
    data = json.loads(result)
    assert len(data["labor_forecast"]) == 1
    fc = data["labor_forecast"][0]
    assert fc["trade"] == "electrical"
    assert fc["gap"] == 6
    assert fc["critical"] is True


def test_unknown_action():
    """Unknown action returns error."""
    tool = WorkforceQuery()
    result = tool.execute(
        action="roster", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "unknown action" in result
