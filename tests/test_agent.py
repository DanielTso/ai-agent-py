"""Tests for the Agent class and tools."""

from unittest.mock import MagicMock, patch

from ai_agent.agent import Agent
from ai_agent.config import Settings
from ai_agent.tools import Calculator, CurrentTime, ToolRegistry, WebSearch


def make_settings(**overrides) -> Settings:
    defaults = {
        "anthropic_api_key": "test-key",
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 100,
    }
    defaults.update(overrides)
    return Settings(**defaults)


# --- Tool & Registry tests ---


def test_tool_registry_register_and_get():
    registry = ToolRegistry()
    calc = Calculator()
    registry.register(calc)

    assert len(registry) == 1
    assert registry.get("calculator") is calc
    assert registry.get("nonexistent") is None


def test_tool_registry_to_api_format():
    registry = ToolRegistry()
    registry.register(Calculator())
    registry.register(CurrentTime())

    api_tools = registry.to_api_format()
    assert len(api_tools) == 2
    names = {t["name"] for t in api_tools}
    assert names == {"calculator", "current_time"}
    for t in api_tools:
        assert "description" in t
        assert "input_schema" in t


def test_calculator_basic_ops():
    calc = Calculator()
    assert calc.execute(expression="2 + 3") == "5"
    assert calc.execute(expression="10 / 4") == "2.5"
    assert calc.execute(expression="2 ** 10") == "1024"
    assert calc.execute(expression="7 % 3") == "1"
    assert calc.execute(expression="7 // 2") == "3"


def test_calculator_rejects_unsafe():
    calc = Calculator()
    result = calc.execute(expression="__import__('os').system('echo hi')")
    assert result.startswith("Error:")


def test_current_time():
    time_tool = CurrentTime()
    result = time_tool.execute()
    assert "UTC" in result


def test_tool_to_api_format():
    calc = Calculator()
    fmt = calc.to_api_format()
    assert fmt["name"] == "calculator"
    assert "description" in fmt
    assert fmt["input_schema"]["type"] == "object"


# --- WebSearch tests ---


def test_web_search_schema():
    ws = WebSearch()
    schema = ws.get_input_schema()
    assert schema["type"] == "object"
    assert "query" in schema["properties"]
    assert schema["required"] == ["query"]


def test_web_search_to_api_format():
    ws = WebSearch()
    fmt = ws.to_api_format()
    assert fmt["name"] == "web_search"
    assert "description" in fmt
    assert fmt["input_schema"]["required"] == ["query"]


def test_web_search_execute():
    ws = WebSearch()
    mock_results = [
        {
            "title": "Python News",
            "href": "https://example.com/python",
            "body": "Latest Python updates.",
        },
        {
            "title": "Python 3.13",
            "href": "https://example.com/py313",
            "body": "Python 3.13 released.",
        },
    ]
    with patch("ai_agent.tools.DDGS") as mock_ddgs_cls:
        mock_ddgs_cls.return_value.text.return_value = mock_results
        result = ws.execute(query="Python news")

    assert "Python News" in result
    assert "https://example.com/python" in result
    assert "Latest Python updates." in result
    assert "Python 3.13" in result


def test_web_search_no_results():
    ws = WebSearch()
    with patch("ai_agent.tools.DDGS") as mock_ddgs_cls:
        mock_ddgs_cls.return_value.text.return_value = []
        result = ws.execute(query="xyznonexistent")

    assert result == "No results found."


def test_web_search_error():
    ws = WebSearch()
    with patch("ai_agent.tools.DDGS") as mock_ddgs_cls:
        mock_ddgs_cls.return_value.text.side_effect = Exception("Network error")
        result = ws.execute(query="test")

    assert result.startswith("Error performing search:")
    assert "Network error" in result


# --- Agent tests (no tools) ---


def test_agent_chat():
    settings = make_settings()

    with patch("ai_agent.agent.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "Hello back!"

        mock_response = MagicMock()
        mock_response.content = [text_block]
        mock_response.stop_reason = "end_of_turn"
        mock_client.messages.create.return_value = mock_response

        agent = Agent(settings=settings)
        result = agent.chat("Hello")

        assert result == "Hello back!"
        assert len(agent.conversation) == 2
        assert agent.conversation[0] == {"role": "user", "content": "Hello"}


def test_agent_reset():
    settings = make_settings()

    with patch("ai_agent.agent.Anthropic"):
        agent = Agent(settings=settings)
        agent.conversation = [{"role": "user", "content": "test"}]
        agent.reset()
        assert agent.conversation == []


# --- Agent agentic loop tests ---


def test_agent_tool_use_loop():
    """Verify the agent executes a tool and makes a follow-up API call."""
    settings = make_settings()
    registry = ToolRegistry()
    registry.register(Calculator())

    with patch("ai_agent.agent.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        # First response: Claude requests tool use
        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.name = "calculator"
        tool_use_block.input = {"expression": "2 + 2"}
        tool_use_block.id = "tool_abc123"

        tool_response = MagicMock()
        tool_response.content = [tool_use_block]
        tool_response.stop_reason = "tool_use"

        # Second response: Claude returns final text
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "The answer is 4."

        final_response = MagicMock()
        final_response.content = [text_block]
        final_response.stop_reason = "end_of_turn"

        mock_client.messages.create.side_effect = [tool_response, final_response]

        agent = Agent(settings=settings, tool_registry=registry)
        result = agent.chat("What is 2 + 2?")

        assert result == "The answer is 4."
        assert mock_client.messages.create.call_count == 2

        # Verify tool was executed and result tracked
        assert len(agent.last_tool_calls) == 1
        assert agent.last_tool_calls[0]["tool"] == "calculator"
        assert agent.last_tool_calls[0]["result"] == "4"

        # Verify tool_result was sent back in conversation
        tool_result_msg = agent.conversation[2]  # user -> assistant(tool_use) -> user(tool_result)
        assert tool_result_msg["role"] == "user"
        assert tool_result_msg["content"][0]["type"] == "tool_result"
        assert tool_result_msg["content"][0]["tool_use_id"] == "tool_abc123"
        assert tool_result_msg["content"][0]["content"] == "4"


def test_agent_unknown_tool():
    """If Claude requests an unknown tool, return an error message."""
    settings = make_settings()
    registry = ToolRegistry()
    # Don't register any tools — but pass the registry so the agent sends tools=[]

    with patch("ai_agent.agent.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.name = "nonexistent"
        tool_use_block.input = {}
        tool_use_block.id = "tool_xyz"

        tool_response = MagicMock()
        tool_response.content = [tool_use_block]
        tool_response.stop_reason = "tool_use"

        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "Sorry, that tool is not available."

        final_response = MagicMock()
        final_response.content = [text_block]
        final_response.stop_reason = "end_of_turn"

        mock_client.messages.create.side_effect = [tool_response, final_response]

        # Register one tool so tools list is non-empty (otherwise tools won't be sent)
        registry.register(CurrentTime())
        agent = Agent(settings=settings, tool_registry=registry)
        result = agent.chat("Use nonexistent tool")

        assert result == "Sorry, that tool is not available."
        assert agent.last_tool_calls[0]["result"].startswith("Error:")
