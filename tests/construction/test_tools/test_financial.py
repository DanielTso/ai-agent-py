"""Tests for the financial query tool."""

import json

from construction.tools.financial import FinancialQuery


def test_schema():
    """Tool schema has required fields."""
    tool = FinancialQuery()
    assert tool.name == "financial_query"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "period" in props
    assert "data" in props
    assert props["action"]["enum"] == [
        "budget_status",
        "earned_value",
        "cash_flow",
        "change_orders",
    ]
    assert schema["required"] == ["action", "project_id"]


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = FinancialQuery()
    fmt = tool.to_api_format()
    assert fmt["name"] == "financial_query"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_budget_status():
    """budget_status returns realistic budget data."""
    tool = FinancialQuery()
    result = tool.execute(
        action="budget_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert data["project_id"] == "PRJ-001"
    assert data["total_budget"] == 45_000_000.00
    assert data["spent_to_date"] > 0
    assert data["committed"] > 0
    assert data["forecast_at_completion"] > 0
    assert data["contingency_remaining"] > 0
    assert "variance_pct" in data


def test_earned_value():
    """earned_value returns EVM metrics."""
    tool = FinancialQuery()
    result = tool.execute(
        action="earned_value", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "bcws" in data
    assert "bcwp" in data
    assert "acwp" in data
    assert "cpi" in data
    assert "spi" in data
    assert "eac" in data
    assert "etc" in data
    assert "vac" in data
    assert "tcpi" in data
    assert data["cpi"] == 0.987
    assert data["spi"] == 0.925


def test_cash_flow_all():
    """cash_flow returns all periods."""
    tool = FinancialQuery()
    result = tool.execute(
        action="cash_flow", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "cash_flow" in data
    assert len(data["cash_flow"]) == 3
    period = data["cash_flow"][0]
    assert "period" in period
    assert "planned_draw" in period
    assert "actual_draw" in period
    assert "cumulative_planned" in period
    assert "cumulative_actual" in period


def test_cash_flow_filtered():
    """cash_flow filters by period."""
    tool = FinancialQuery()
    result = tool.execute(
        action="cash_flow",
        project_id="PRJ-001",
        period="2025-Q2",
    )
    data = json.loads(result)
    assert len(data["cash_flow"]) == 1
    assert data["cash_flow"][0]["period"] == "2025-Q2"


def test_change_orders():
    """change_orders returns pending and approved orders."""
    tool = FinancialQuery()
    result = tool.execute(
        action="change_orders", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "change_orders" in data
    assert len(data["change_orders"]) == 3
    co = data["change_orders"][0]
    assert "id" in co
    assert "co_number" in co
    assert "description" in co
    assert "cost_impact" in co
    assert "schedule_impact_days" in co
    assert "status" in co


def test_unknown_action():
    """Unknown action returns error."""
    tool = FinancialQuery()
    result = tool.execute(
        action="forecast", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "unknown action" in result
