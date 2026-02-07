"""Tests for the OSHA search tool."""

import json

from construction.tools.osha import OshaSearch


def test_schema():
    """Tool schema has expected properties."""
    tool = OshaSearch()
    assert tool.name == "osha_search"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "establishment" in props
    assert "state" in props
    assert "sic_code" in props
    assert "date_from" in props
    assert "date_to" in props


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = OshaSearch()
    fmt = tool.to_api_format()
    assert fmt["name"] == "osha_search"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_execute_default():
    """Execute returns mock inspections with violations."""
    tool = OshaSearch()
    result = tool.execute()
    data = json.loads(result)
    assert "inspections" in data
    assert data["total_results"] == 2
    assert "note" in data
    # Check inspection structure
    insp = data["inspections"][0]
    assert "inspection_number" in insp
    assert "violations" in insp
    assert len(insp["violations"]) > 0
    # Check violation structure
    viol = insp["violations"][0]
    assert "standard" in viol
    assert "type" in viol
    assert "penalty" in viol


def test_execute_with_establishment():
    """Execute filters by establishment name."""
    tool = OshaSearch()
    result = tool.execute(establishment="XYZ Builders")
    data = json.loads(result)
    for insp in data["inspections"]:
        assert insp["establishment"] == "XYZ Builders"


def test_execute_with_state():
    """Execute uses provided state."""
    tool = OshaSearch()
    result = tool.execute(state="CA")
    data = json.loads(result)
    for insp in data["inspections"]:
        assert insp["state"] == "CA"


def test_execute_records_query():
    """Query parameters are recorded in the response."""
    tool = OshaSearch()
    result = tool.execute(
        establishment="Test Corp",
        state="NY",
        sic_code="1542",
        date_from="2025-01-01",
        date_to="2025-12-31",
    )
    data = json.loads(result)
    query = data["query"]
    assert query["establishment"] == "Test Corp"
    assert query["state"] == "NY"
    assert query["sic_code"] == "1542"
    assert query["date_from"] == "2025-01-01"
    assert query["date_to"] == "2025-12-31"


def test_execute_error_handling():
    """Execute returns error string on exception."""
    tool = OshaSearch()
    # Force an error by making _mock_search raise
    original = tool._mock_search
    tool._mock_search = lambda **kw: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute()
    assert "Error" in result
    assert "DB unavailable" in result
    tool._mock_search = original
