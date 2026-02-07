"""Tests for the environmental query tool."""

import json

from construction.tools.environmental import EnvironmentalQuery


def test_schema():
    """Tool schema has expected properties."""
    tool = EnvironmentalQuery()
    assert tool.name == "environmental_query"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "permit_type" in props
    assert set(props["action"]["enum"]) == {
        "permits",
        "leed_credits",
        "carbon",
        "swppp_check",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = EnvironmentalQuery()
    fmt = tool.to_api_format()
    assert fmt["name"] == "environmental_query"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_permits():
    """Permits action returns permit data."""
    tool = EnvironmentalQuery()
    result = tool.execute(
        action="permits", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "permits" in data
    permits = data["permits"]
    assert len(permits) == 4
    assert permits[0]["permit_type"] == "SWPPP"


def test_permits_filter():
    """Permits can be filtered by type."""
    tool = EnvironmentalQuery()
    result = tool.execute(
        action="permits",
        project_id="PRJ-001",
        permit_type="air",
    )
    data = json.loads(result)
    permits = data["permits"]
    assert len(permits) == 1
    assert permits[0]["permit_type"] == "air"
    assert permits[0]["status"] == "expiring"


def test_leed_credits():
    """LEED credits returns credit tracking data."""
    tool = EnvironmentalQuery()
    result = tool.execute(
        action="leed_credits", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "leed_credits" in data
    assert "total_points" in data
    credits = data["leed_credits"]
    assert len(credits) == 5
    assert data["total_points"] == 13.0


def test_carbon():
    """Carbon action returns emissions data."""
    tool = EnvironmentalQuery()
    result = tool.execute(
        action="carbon", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "carbon_metrics" in data
    metrics = data["carbon_metrics"]
    assert len(metrics) == 4


def test_swppp_check():
    """SWPPP check returns inspection data."""
    tool = EnvironmentalQuery()
    result = tool.execute(
        action="swppp_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "swppp_checks" in data
    checks = data["swppp_checks"]
    assert len(checks) == 2
    assert checks[0]["compliant"] is True
    assert checks[1]["compliant"] is False


def test_unknown_action():
    """Unknown action returns error string."""
    tool = EnvironmentalQuery()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = EnvironmentalQuery()
    original = tool._permits
    tool._permits = lambda *a: (_ for _ in ()).throw(
        RuntimeError("API unavailable")
    )
    result = tool.execute(
        action="permits", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "API unavailable" in result
    tool._permits = original
