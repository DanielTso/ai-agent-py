# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

- **Install dependencies**: `uv sync`
- **Run the CLI agent**: `uv run ai-agent` (interactive REPL)
- **Run the Construction PM server**: `uv run construction-pm` (FastAPI on port 8000)
- **Run all tests**: `uv run pytest`
- **Run a single test**: `uv run pytest tests/test_agent.py::test_agent_chat`
- **Run construction tests only**: `uv run pytest tests/construction/`
- **Run tests by category**:
  - Agents: `uv run pytest tests/construction/test_agents/`
  - Tools: `uv run pytest tests/construction/test_tools/`
  - API: `uv run pytest tests/construction/test_api/`
  - Integrations: `uv run pytest tests/construction/test_integrations/`
  - E2E: `uv run pytest tests/construction/test_e2e_*.py`
- **Lint**: `uv run ruff check src tests`
- **Lint with auto-fix**: `uv run ruff check --fix src tests`
- **Format**: `uv run ruff format src tests`
- **Add a dependency**: `uv add <package>`
- **Add a dev dependency**: `uv add --group dev <package>`
- **Start infrastructure**: `docker compose up -d postgres redis`
- **Run migrations**: `uv run alembic upgrade head`
- **Full stack**: `docker compose up --build`

## Architecture

Two packages in a src-layout: the original CLI agent (`src/ai_agent/`) and the construction PM ecosystem (`src/construction/`).

### Core Agent (`src/ai_agent/`)

```
src/ai_agent/
├── config.py    # Settings via pydantic-settings (ANTHROPIC_API_KEY, MODEL, MAX_TOKENS)
├── tools.py     # Tool ABC, ToolRegistry, built-in tools (Calculator, CurrentTime, WebSearch)
├── agent.py     # Core Agent class: agentic loop with tool use + optional system_prompt
├── main.py      # CLI entrypoint: interactive REPL loop
```

- **Tool ABC** (`tools.py`): `name`, `description`, `get_input_schema()`, `execute(**kwargs)`. All construction tools also subclass this.
- **Agent** (`agent.py`): Stateful class with agentic loop. Accepts optional `system_prompt` parameter for specialized personas.

### Construction PM Ecosystem (`src/construction/`)

```
src/construction/
├── config.py                  # ConstructionSettings (35+ env vars)
├── db/
│   ├── engine.py              # SQLAlchemy async engine + session factory
│   ├── models.py              # 27+ ORM models (pgvector for embeddings)
│   ├── repositories.py        # CRUD data access layer
│   └── seed.py                # Demo data (transformer delay scenario)
├── redis_/
│   ├── client.py              # Connection pool
│   ├── pubsub.py              # Inter-agent pub/sub (9 channels)
│   └── shared_memory.py       # Typed shared state (risks, alerts, safety, etc.)
├── agents/
│   ├── base.py                # ConstructionAgent ABC
│   ├── orchestrator.py        # Rule-based coordinator (NOT AI-powered)
│   ├── risk_forecaster.py     # Tier 1: hourly risk prediction
│   ├── document_intelligence.py  # Tier 1: semantic doc search
│   ├── critical_path.py       # Tier 1: Monte Carlo schedule optimization
│   ├── compliance_verifier.py # Tier 1: BIM/code compliance
│   ├── supply_chain.py        # Tier 1: vendor/shipment monitoring
│   ├── financial_intelligence.py  # Tier 2: EVM, cash flow, change orders
│   ├── stakeholder_communication.py  # Tier 2: auto-draft reports/notices
│   ├── workforce_labor.py     # Tier 2: crew productivity, certifications
│   ├── commissioning_turnover.py  # Tier 3: IST sequencing, punch lists
│   ├── environmental_sustainability.py  # Tier 3: SWPPP, LEED, carbon
│   ├── claims_dispute.py      # Tier 3: contemporaneous records, delay analysis
│   ├── site_logistics.py      # Tier 3: crane/staging/headcount
│   └── safety_compliance.py   # Tier 3: OSHA/MSHA/NIOSH
├── tools/                     # 23 tools (all subclass Tool ABC)
├── schemas/                   # 15 Pydantic schema modules
├── integrations/              # 13 external API clients
├── api/
│   ├── app.py                 # FastAPI factory + health endpoint
│   ├── deps.py                # Dependency injection
│   ├── websocket.py           # WebSocket ConnectionManager
│   └── routers/               # 16 routers (risks, schedule, safety, etc.)
└── tasks/
    ├── celery_app.py          # Celery + Redis broker
    └── scheduled.py           # Cron schedules for all 13 agents
```

### Frontend (`frontend/`)

Next.js 15 + TypeScript + Tailwind with 15 dashboard pages, 11 dashboard components, WebSocket live updates, and API client matching all backend endpoints.

## Adding a New Tool

1. Subclass `Tool` in the appropriate file under `src/construction/tools/` (or `src/ai_agent/tools.py` for core tools)
2. Implement `name`, `description`, `get_input_schema()`, `execute(**kwargs)`
3. Register in the agent's `_register_tools()` method
4. Wrap external calls in try/except, returning `f"Error: {exc}"` strings
5. For long description strings, use parenthesized concatenation to stay under 100-char line limit

## Adding a New Construction Agent

1. Subclass `ConstructionAgent` in `src/construction/agents/`
2. Set class attributes: `name`, `description`, `schedule`
3. Implement `_register_tools()` — register tools specific to this agent
4. Implement `get_system_prompt()` — return the agent's persona/instructions
5. Implement `async run(context)` — execute the agent's primary task, return `AgentEvent`
6. Add cross-agent trigger rules in `orchestrator.py` if needed
7. Add a Celery task in `tasks/scheduled.py` with the appropriate schedule
8. Create a test file in `tests/construction/test_agents/`

## Orchestrator Cross-Agent Rules

The orchestrator (`agents/orchestrator.py`) is rule-based (not AI-powered). Key patterns:
- Supply chain delay → Critical Path reoptimize + Financial assess + Claims log
- Safety stop-work → IMMEDIATE SMS + Critical Path hold + Site Logistics restrict
- Document contradiction → Compliance check + Communication draft RFI
- Budget variance >10% → Risk reassess + Communication draft owner report
- Escalation threshold: >$250k impact OR safety-critical → SMS to PM

## Code Style

- Ruff: 100-char line length, Python 3.12 target
- Lint rules: `E`, `F`, `I` (isort), `N` (naming), `UP` (pyupgrade), `RUF`
- pytest with `asyncio_mode = "auto"` for async tests
- Parenthesized string concatenation for long descriptions

## Testing Patterns

- **Core agent**: Mock Anthropic client with `patch("ai_agent.agent.Anthropic")`
- **Construction agents**: Mock via `patch("construction.agents.base.Agent")`, use `AsyncMock` for async methods
- **Tools**: Test `get_input_schema()`, all action branches, error handling
- **API routers**: Use `httpx.AsyncClient` with `ASGITransport(app=app)`
- **Integration clients**: Mock `httpx` responses, test retry/error handling
- **Shared fixtures**: `conftest.py` provides `mock_construction_settings`, `mock_shared_memory`, `mock_pubsub`

## Key Scope Boundaries (Agent Roles)

| Concern | Owns It | Does NOT Touch |
|---------|---------|----------------|
| Risk prediction | Risk Forecaster | Does not create tickets or schedule changes |
| Document answers | Document Intelligence | Does not modify documents |
| Schedule changes | Critical Path Optimizer | Never auto-applies (creates approval requests) |
| BIM/code compliance | Compliance Verifier | Does not do safety regulation checks |
| OSHA/MSHA/NIOSH | Safety Compliance | Only agent that can recommend stop-work |
| Budget/cost | Financial Intelligence | Does not approve spend |
| External comms | Stakeholder Communication | Does not make decisions, only drafts |
| Site operations | Site Logistics | Does not enforce safety |

## Infrastructure

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI + Uvicorn |
| AI Engine | Anthropic Claude API |
| Database | PostgreSQL 16 + pgvector |
| Cache/Messaging | Redis 7 (pub/sub, shared memory, dedup) |
| Task Scheduler | Celery + Redis broker |
| Frontend | Next.js 15 + TypeScript + Tailwind + Recharts |
| Containerization | Docker Compose |
