"""Tests for the hazard analysis tool."""

import json

from construction.tools.hazard_analysis import HazardAnalysis


def test_schema():
    """Tool schema has expected properties."""
    tool = HazardAnalysis()
    assert tool.name == "hazard_analysis"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "activity" in props
    assert "location" in props
    assert set(props["action"]["enum"]) == {
        "generate_jha",
        "risk_assessment",
        "hierarchy_of_controls",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = HazardAnalysis()
    fmt = tool.to_api_format()
    assert fmt["name"] == "hazard_analysis"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_generate_jha_steel():
    """JHA for steel erection returns hazards and controls."""
    tool = HazardAnalysis()
    result = tool.execute(
        action="generate_jha",
        activity="steel_erection",
    )
    data = json.loads(result)
    assert "jha_entries" in data
    entries = data["jha_entries"]
    assert len(entries) == 2
    entry = entries[0]
    assert "hazards" in entry
    assert "controls" in entry
    assert "ppe_required" in entry
    assert entry["competent_person_required"] is True


def test_generate_jha_excavation():
    """JHA for excavation returns correct data."""
    tool = HazardAnalysis()
    result = tool.execute(
        action="generate_jha",
        activity="excavation",
    )
    data = json.loads(result)
    entries = data["jha_entries"]
    assert len(entries) == 1
    assert "Cave-in" in entries[0]["hazards"]


def test_generate_jha_default():
    """JHA defaults to steel_erection for unknown activity."""
    tool = HazardAnalysis()
    result = tool.execute(
        action="generate_jha",
        activity="unknown_activity",
    )
    data = json.loads(result)
    assert "jha_entries" in data


def test_risk_assessment():
    """Risk assessment returns risk matrix."""
    tool = HazardAnalysis()
    result = tool.execute(
        action="risk_assessment",
        activity="steel_erection",
        location="Building A Level 5",
    )
    data = json.loads(result)
    assert "risk_assessment" in data
    ra = data["risk_assessment"]
    assert "risk_matrix" in ra
    assert ra["location"] == "Building A Level 5"
    assert len(ra["risk_matrix"]) == 3


def test_hierarchy_of_controls():
    """Hierarchy of controls returns 5 levels."""
    tool = HazardAnalysis()
    result = tool.execute(
        action="hierarchy_of_controls",
        activity="steel_erection",
    )
    data = json.loads(result)
    assert "hierarchy_of_controls" in data
    hoc = data["hierarchy_of_controls"]
    assert len(hoc["hierarchy"]) == 5
    assert hoc["hierarchy"][0]["type"] == "Elimination"
    assert hoc["hierarchy"][4]["type"] == "PPE"


def test_unknown_action():
    """Unknown action returns error string."""
    tool = HazardAnalysis()
    result = tool.execute(action="invalid")
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = HazardAnalysis()
    original = tool._generate_jha
    tool._generate_jha = lambda *a: (_ for _ in ()).throw(
        RuntimeError("Analysis failed")
    )
    result = tool.execute(action="generate_jha")
    assert "Error" in result
    assert "Analysis failed" in result
    tool._generate_jha = original
