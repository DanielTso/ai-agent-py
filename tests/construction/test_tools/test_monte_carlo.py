"""Tests for the MonteCarloSimulationTool."""

import json

from construction.tools.monte_carlo import MonteCarloSimulationTool


def test_monte_carlo_schema():
    tool = MonteCarloSimulationTool()
    schema = tool.get_input_schema()
    assert schema["type"] == "object"
    assert "project_id" in schema["properties"]
    assert "iterations" in schema["properties"]
    assert schema["required"] == ["project_id"]


def test_monte_carlo_api_format():
    tool = MonteCarloSimulationTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "monte_carlo_simulation"
    assert "description" in fmt


def test_simulation_runs_with_numpy():
    """Verify the simulation actually runs and returns valid distribution data."""
    tool = MonteCarloSimulationTool()
    result = tool.execute(
        project_id="PROJ-001", iterations=1000
    )
    data = json.loads(result)

    assert data["project_id"] == "PROJ-001"
    assert data["iterations"] == 1000
    assert data["p50_completion"] != ""
    assert data["p80_completion"] != ""
    assert data["p95_completion"] != ""
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["float_consumed"], dict)
    assert len(data["float_consumed"]) > 0
    assert isinstance(data["histogram"], list)
    assert len(data["histogram"]) == 10
    assert "run_at" in data


def test_simulation_percentile_ordering():
    """P50 <= P80 <= P95 completion dates."""
    tool = MonteCarloSimulationTool()
    result = tool.execute(
        project_id="PROJ-001", iterations=5000
    )
    data = json.loads(result)

    assert data["p50_completion"] <= data["p80_completion"]
    assert data["p80_completion"] <= data["p95_completion"]


def test_simulation_histogram_sums_to_iterations():
    """Histogram bin counts should sum to total iterations."""
    tool = MonteCarloSimulationTool()
    iterations = 2000
    result = tool.execute(
        project_id="PROJ-001", iterations=iterations
    )
    data = json.loads(result)

    total_count = sum(
        b["count"] for b in data["histogram"]
    )
    assert total_count == iterations


def test_simulation_with_overrides():
    """Test with custom activity duration overrides."""
    tool = MonteCarloSimulationTool()
    result = tool.execute(
        project_id="PROJ-001",
        iterations=1000,
        activity_durations={
            "Foundation Pour": {
                "min": 12,
                "mode": 16,
                "max": 24,
            },
        },
    )
    data = json.loads(result)
    assert data["iterations"] == 1000
    assert data["p50_completion"] != ""


def test_simulation_custom_confidence_levels():
    """Test with custom confidence levels."""
    tool = MonteCarloSimulationTool()
    result = tool.execute(
        project_id="PROJ-001",
        iterations=1000,
        confidence_levels=[0.25, 0.5, 0.75],
    )
    data = json.loads(result)
    # Should still have results (keys mapped from levels)
    assert data["iterations"] == 1000
    assert "run_at" in data


def test_simulation_float_consumed_has_entries():
    """Float consumed should have entries for activities."""
    tool = MonteCarloSimulationTool()
    result = tool.execute(
        project_id="PROJ-001", iterations=1000
    )
    data = json.loads(result)

    fc = data["float_consumed"]
    assert "Foundation Pour" in fc
    assert "Commissioning" in fc
    # Non-critical activities also tracked
    assert "Exterior Envelope" in fc
