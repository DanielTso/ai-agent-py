# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

- **Install dependencies**: `uv sync`
- **Run the agent**: `uv run ai-agent` (CLI entrypoint) or `uv run python -m ai_agent.main`
- **Run all tests**: `uv run pytest`
- **Run a single test**: `uv run pytest tests/test_agent.py::test_agent_chat`
- **Lint**: `uv run ruff check src tests`
- **Lint with auto-fix**: `uv run ruff check --fix src tests`
- **Format**: `uv run ruff format src tests`
- **Add a dependency**: `uv add <package>`
- **Add a dev dependency**: `uv add --group dev <package>`

## Architecture

This is a Python AI agent using the Anthropic Claude API with a src-layout package structure.

```
src/ai_agent/
├── config.py    # Settings via pydantic-settings, loaded from env vars / .env
├── tools.py     # Tool ABC, ToolRegistry, built-in tools (Calculator, CurrentTime, WebSearch)
├── agent.py     # Core Agent class: agentic loop with tool use
├── main.py      # CLI entrypoint: interactive REPL loop, registers tools
```

- **Tools** (`tools.py`): `Tool` ABC defines `name`, `description`, `get_input_schema()`, `execute(**kwargs)`. `ToolRegistry` holds tools and converts to Anthropic API format via `to_api_format()`. New tools subclass `Tool` and are registered in `main.py`.
- **Agent** (`agent.py`): Stateful class with an agentic loop — `chat()` calls Claude, executes any requested tools, feeds results back, and repeats until Claude produces a final text response.
- **Settings** (`config.py`): Uses `pydantic-settings.BaseSettings` to load `ANTHROPIC_API_KEY`, `MODEL`, and `MAX_TOKENS` from environment or `.env` file. Copy `.env.example` to `.env` to configure.

## Adding a New Tool

1. Subclass `Tool` in `tools.py` — implement `name`, `description`, `get_input_schema()`, `execute(**kwargs)`
2. Register it in `main.py`: `registry.register(YourTool())`
3. Wrap external calls in try/except, returning `f"Error: {exc}"` strings
4. For long description strings, use parenthesized concatenation to stay under 100-char line limit

## Code Style

- Ruff is configured with 100-char line length, Python 3.12 target
- Lint rules: `E`, `F`, `I` (isort), `N` (naming), `UP` (pyupgrade), `RUF`
- pytest with `asyncio_mode = "auto"` for async tests

## Testing Patterns

- Tests mock the Anthropic client: `patch("ai_agent.agent.Anthropic")`
- External tool dependencies are mocked at module level: e.g. `patch("ai_agent.tools.DDGS")`
- Use `make_settings()` helper in tests to create a `Settings` with a fake API key
