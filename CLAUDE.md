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
├── agent.py     # Core Agent class: manages Anthropic client and conversation history
├── main.py      # CLI entrypoint: interactive REPL loop
```

- **Agent** (`agent.py`): Stateful class that holds an `Anthropic` client and a conversation list. `chat()` appends messages and calls `messages.create()`. `reset()` clears history.
- **Settings** (`config.py`): Uses `pydantic-settings.BaseSettings` to load `ANTHROPIC_API_KEY`, `MODEL`, and `MAX_TOKENS` from environment or `.env` file. Copy `.env.example` to `.env` to configure.

## Code Style

- Ruff is configured with 100-char line length, Python 3.12 target
- Lint rules: `E`, `F`, `I` (isort), `N` (naming), `UP` (pyupgrade), `RUF`
- pytest with `asyncio_mode = "auto"` for async tests
