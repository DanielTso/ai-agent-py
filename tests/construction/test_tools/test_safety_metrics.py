"""Tests for the safety metrics tool."""

import json

from construction.tools.safety_metrics import SafetyMetrics


def test_schema():
    """Tool schema has expected properties."""
    tool = SafetyMetrics()
    assert tool.name == "safety_metrics"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "total_recordable_cases" in props
    assert "dart_cases" in props
    assert "hours_worked" in props
    assert set(props["action"]["enum"]) == {
        "calculate_trir",
        "calculate_dart",
        "calculate_emr",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = SafetyMetrics()
    fmt = tool.to_api_format()
    assert fmt["name"] == "safety_metrics"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_calculate_trir():
    """TRIR calculation returns correct value."""
    tool = SafetyMetrics()
    result = tool.execute(
        action="calculate_trir",
        total_recordable_cases=2,
        hours_worked=200000,
    )
    data = json.loads(result)
    assert data["metric"] == "TRIR"
    assert data["trir"] == 2.0
    assert data["status"] == "below_benchmark"


def test_calculate_trir_above_benchmark():
    """TRIR above benchmark returns correct status."""
    tool = SafetyMetrics()
    result = tool.execute(
        action="calculate_trir",
        total_recordable_cases=10,
        hours_worked=200000,
    )
    data = json.loads(result)
    assert data["trir"] == 10.0
    assert data["status"] == "above_benchmark"


def test_calculate_trir_defaults():
    """TRIR uses defaults when no params given."""
    tool = SafetyMetrics()
    result = tool.execute(action="calculate_trir")
    data = json.loads(result)
    assert data["metric"] == "TRIR"
    assert "trir" in data


def test_calculate_dart():
    """DART calculation returns correct value."""
    tool = SafetyMetrics()
    result = tool.execute(
        action="calculate_dart",
        dart_cases=1,
        hours_worked=200000,
    )
    data = json.loads(result)
    assert data["metric"] == "DART"
    assert data["dart_rate"] == 1.0
    assert data["status"] == "below_benchmark"


def test_calculate_emr():
    """EMR returns experience modification rate."""
    tool = SafetyMetrics()
    result = tool.execute(
        action="calculate_emr",
        project_id="PRJ-001",
    )
    data = json.loads(result)
    assert data["metric"] == "EMR"
    assert data["emr"] == 0.87
    assert "components" in data


def test_unknown_action():
    """Unknown action returns error string."""
    tool = SafetyMetrics()
    result = tool.execute(action="invalid")
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = SafetyMetrics()
    original = tool._calculate_trir
    tool._calculate_trir = lambda *a: (_ for _ in ()).throw(
        RuntimeError("Calc error")
    )
    result = tool.execute(action="calculate_trir")
    assert "Error" in result
    assert "Calc error" in result
    tool._calculate_trir = original
