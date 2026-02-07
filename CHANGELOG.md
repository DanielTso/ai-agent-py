# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-06

### Added
- Initial project setup with Anthropic Claude API integration
- Interactive CLI REPL via `uv run ai-agent`
- Configuration via pydantic-settings with `.env` support
- Tool system with `ToolRegistry` for managing agent tools
- `Calculator` tool for safe arithmetic expression evaluation
- `CurrentTime` tool for UTC date/time
- `WebSearch` tool using DuckDuckGo (no API key required)
- Agentic loop for multi-step tool use conversations
- Test suite with mocked API and tool tests
