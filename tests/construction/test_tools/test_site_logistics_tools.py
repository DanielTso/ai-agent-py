"""Tests for the site logistics query tool."""

import json

from construction.tools.site_logistics_tools import (
    SiteLogisticsQuery,
)


def test_schema():
    """Tool schema has expected properties."""
    tool = SiteLogisticsQuery()
    assert tool.name == "site_logistics_query"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "date" in props
    assert "trade" in props
    assert set(props["action"]["enum"]) == {
        "crane_schedule",
        "staging",
        "headcount",
        "permits",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = SiteLogisticsQuery()
    fmt = tool.to_api_format()
    assert fmt["name"] == "site_logistics_query"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_crane_schedule():
    """Crane schedule returns time slots."""
    tool = SiteLogisticsQuery()
    result = tool.execute(
        action="crane_schedule", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "crane_schedule" in data
    entries = data["crane_schedule"]
    assert len(entries) == 5
    assert entries[0]["crane_id"] == "TC-01"
    assert entries[0]["weight_tons"] > 0


def test_staging():
    """Staging returns zone utilization data."""
    tool = SiteLogisticsQuery()
    result = tool.execute(
        action="staging", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "staging_zones" in data
    zones = data["staging_zones"]
    assert len(zones) == 3
    assert zones[2]["utilization_pct"] == 95.0


def test_headcount():
    """Headcount returns trade-level data."""
    tool = SiteLogisticsQuery()
    result = tool.execute(
        action="headcount", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "headcount" in data
    counts = data["headcount"]
    assert len(counts) == 4


def test_headcount_trade_filter():
    """Headcount can be filtered by trade."""
    tool = SiteLogisticsQuery()
    result = tool.execute(
        action="headcount",
        project_id="PRJ-001",
        trade="steel",
    )
    data = json.loads(result)
    counts = data["headcount"]
    assert len(counts) == 1
    assert counts[0]["trade"] == "steel"


def test_permits():
    """Permits returns site permit data."""
    tool = SiteLogisticsQuery()
    result = tool.execute(
        action="permits", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "site_permits" in data
    permits = data["site_permits"]
    assert len(permits) == 3
    assert permits[1]["type"] == "crane_permit"


def test_unknown_action():
    """Unknown action returns error string."""
    tool = SiteLogisticsQuery()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = SiteLogisticsQuery()
    original = tool._crane_schedule
    tool._crane_schedule = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="crane_schedule", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._crane_schedule = original
