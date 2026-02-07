"""Tests for the EPA compliance tool."""

import json

from construction.tools.epa_compliance import (
    EpaComplianceTool,
)


def test_schema():
    """Tool schema has expected properties."""
    tool = EpaComplianceTool()
    assert tool.name == "epa_compliance"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "location" in props
    assert "permit_id" in props
    assert set(props["action"]["enum"]) == {
        "npdes_check",
        "air_quality_check",
        "rcra_check",
        "stormwater_check",
        "nepa_status",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = EpaComplianceTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "epa_compliance"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_npdes_check():
    """NPDES check returns permit and discharge data."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="npdes_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "permits" in data
    assert "discharge_monitoring" in data
    assert "exceedances" in data
    assert "compliance_status" in data
    assert "last_sampling_date" in data
    assert data["compliance_status"] == "violation"
    assert len(data["exceedances"]) == 1
    assert data["exceedances"][0]["parameter"] == "Oil & Grease"


def test_npdes_check_with_permit_id():
    """NPDES check uses provided permit_id."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="npdes_check",
        project_id="PRJ-001",
        permit_id="NPDES-CA-0099999",
    )
    data = json.loads(result)
    assert data["permits"][0]["permit_id"] == "NPDES-CA-0099999"


def test_air_quality_check():
    """Air quality check returns readings and controls."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="air_quality_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "ambient_readings" in data
    assert "equipment_emissions" in data
    assert "aqi_index" in data
    assert "exceedances" in data
    assert "control_measures" in data
    assert data["aqi_index"] == 68
    assert len(data["exceedances"]) == 1
    assert len(data["recommended_controls"]) > 0


def test_air_quality_check_with_location():
    """Air quality check uses provided location."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="air_quality_check",
        project_id="PRJ-001",
        location="Denver, CO 80202",
    )
    data = json.loads(result)
    assert data["location"] == "Denver, CO 80202"


def test_rcra_check():
    """RCRA check returns hazardous waste data."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="rcra_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "generator_status" in data
    assert "waste_streams" in data
    assert "manifests" in data
    assert "container_inspections" in data
    assert "violations" in data
    assert data["generator_status"] == "SQG"
    assert len(data["waste_streams"]) == 2
    assert data["waste_streams"][0]["compliant"] is True


def test_stormwater_check():
    """Stormwater check returns SWPPP inspection data."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="stormwater_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "cgp_permit" in data
    assert "swppp_current" in data
    assert "inspection_results" in data
    assert "corrective_actions" in data
    assert "turbidity_monitoring" in data
    assert "rain_events_response" in data
    assert data["swppp_current"] is True
    assert len(data["corrective_actions"]) == 1


def test_nepa_status():
    """NEPA status returns environmental review data."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="nepa_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "review_type" in data
    assert "status" in data
    assert "findings" in data
    assert "mitigation_measures" in data
    assert "public_comment_period" in data
    assert data["review_type"] == "Environmental Assessment"
    assert data["status"] == "FONSI issued"
    assert data["categorical_exclusion"] is False
    assert data["public_comment_period"]["status"] == "closed"


def test_unknown_action():
    """Unknown action returns error string."""
    tool = EpaComplianceTool()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = EpaComplianceTool()
    original = tool._npdes_check
    tool._npdes_check = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="npdes_check", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._npdes_check = original
