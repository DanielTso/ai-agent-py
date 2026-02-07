"""Tests for the claims query tool."""

import json

from construction.tools.claims import ClaimsQuery


def test_schema():
    """Tool schema has expected properties."""
    tool = ClaimsQuery()
    assert tool.name == "claims_query"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "event_id" in props
    assert set(props["action"]["enum"]) == {
        "events",
        "delay_analysis",
        "notices",
        "causation_chain",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = ClaimsQuery()
    fmt = tool.to_api_format()
    assert fmt["name"] == "claims_query"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_events():
    """Events action returns claim event records."""
    tool = ClaimsQuery()
    result = tool.execute(
        action="events", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "claim_events" in data
    events = data["claim_events"]
    assert len(events) == 3
    assert events[0]["event_type"] == "delay"
    assert events[1]["event_type"] == "differing_condition"
    assert events[2]["event_type"] == "force_majeure"


def test_delay_analysis():
    """Delay analysis returns TIA and windows results."""
    tool = ClaimsQuery()
    result = tool.execute(
        action="delay_analysis", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "delay_analyses" in data
    analyses = data["delay_analyses"]
    assert len(analyses) == 2
    assert analyses[0]["analysis_type"] == "TIA"
    assert analyses[0]["critical_delay_days"] == 14.0


def test_notices():
    """Notices action returns notice tracking data."""
    tool = ClaimsQuery()
    result = tool.execute(
        action="notices", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "notices" in data
    notices = data["notices"]
    assert len(notices) == 3
    assert notices[0]["status"] == "acknowledged"
    assert notices[1]["status"] == "pending"


def test_causation_chain():
    """Causation chain returns linked events."""
    tool = ClaimsQuery()
    result = tool.execute(
        action="causation_chain",
        project_id="PRJ-001",
        event_id="CLM-001",
    )
    data = json.loads(result)
    assert "causation_chain" in data
    chain = data["causation_chain"]
    assert "events" in chain
    assert "links" in chain
    assert "root_cause" in chain
    assert len(chain["events"]) > 0


def test_unknown_action():
    """Unknown action returns error string."""
    tool = ClaimsQuery()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = ClaimsQuery()
    original = tool._events
    tool._events = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="events", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._events = original
