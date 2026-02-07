"""Tests for the NIOSH lookup tool."""

import json

from construction.tools.niosh_lookup import NioshLookup


def test_schema():
    """Tool schema has expected properties."""
    tool = NioshLookup()
    assert tool.name == "niosh_lookup"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "substance" in props
    assert "industry" in props
    assert "hazard_type" in props
    assert set(props["action"]["enum"]) == {
        "rel_lookup",
        "face_report",
        "health_hazard",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = NioshLookup()
    fmt = tool.to_api_format()
    assert fmt["name"] == "niosh_lookup"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_rel_lookup_silica():
    """REL lookup returns silica exposure data."""
    tool = NioshLookup()
    result = tool.execute(
        action="rel_lookup", substance="silica"
    )
    data = json.loads(result)
    assert "rel_data" in data
    rel = data["rel_data"]
    assert rel["niosh_rel"] == 0.05
    assert "health_effects" in rel
    assert "controls" in rel


def test_rel_lookup_noise():
    """REL lookup returns noise exposure data."""
    tool = NioshLookup()
    result = tool.execute(
        action="rel_lookup", substance="noise"
    )
    data = json.loads(result)
    rel = data["rel_data"]
    assert rel["niosh_rel"] == 85.0
    assert "dBA" in rel["unit"]


def test_rel_lookup_default():
    """REL lookup defaults to silica for unknown substance."""
    tool = NioshLookup()
    result = tool.execute(
        action="rel_lookup", substance="unknown_chem"
    )
    data = json.loads(result)
    assert "rel_data" in data


def test_face_report():
    """FACE report returns fatality investigation data."""
    tool = NioshLookup()
    result = tool.execute(
        action="face_report",
        industry="construction",
    )
    data = json.loads(result)
    assert "face_reports" in data
    reports = data["face_reports"]
    assert len(reports) == 2
    assert "key_recommendations" in reports[0]


def test_health_hazard():
    """Health hazard returns control hierarchy."""
    tool = NioshLookup()
    result = tool.execute(
        action="health_hazard", hazard_type="noise"
    )
    data = json.loads(result)
    assert "health_hazard" in data
    hazard = data["health_hazard"]
    assert "control_hierarchy" in hazard
    assert "medical_surveillance" in hazard


def test_health_hazard_heat():
    """Health hazard returns heat stress data."""
    tool = NioshLookup()
    result = tool.execute(
        action="health_hazard", hazard_type="heat"
    )
    data = json.loads(result)
    hazard = data["health_hazard"]
    assert "Heat" in hazard["hazard"]


def test_unknown_action():
    """Unknown action returns error string."""
    tool = NioshLookup()
    result = tool.execute(action="invalid")
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = NioshLookup()
    original = tool._rel_lookup
    tool._rel_lookup = lambda *a: (_ for _ in ()).throw(
        RuntimeError("Lookup failed")
    )
    result = tool.execute(
        action="rel_lookup", substance="silica"
    )
    assert "Error" in result
    assert "Lookup failed" in result
    tool._rel_lookup = original
