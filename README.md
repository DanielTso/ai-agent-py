# Construction PM AI

A **13-agent AI ecosystem** for construction project management on mission-critical facilities (Tier III/IV data centers, hospitals, emergency operations centers). Built on Anthropic Claude with a FastAPI backend, Next.js dashboard, and full DevOps stack.

$500k/day penalty exposure. Zero tolerance for operational downtime.

## Agents

| # | Agent | Purpose | Schedule |
|---|-------|---------|----------|
| 1 | **Risk Forecaster** | Predict schedule/cost/safety risks 14+ days ahead | Hourly |
| 2 | **Document Intelligence** | Semantic search across 10k+ docs with construction ontology | On-demand |
| 3 | **Critical Path Optimizer** | Dynamic resequencing + Monte Carlo simulation | On-demand |
| 4 | **Compliance Verifier** | Verify installations against BIM + codes | Twice daily |
| 5 | **Supply Chain Resilience** | Monitor 50+ vendors, track shipments, find alternatives | Every 4h |
| 6 | **Financial Intelligence** | Earned value (CPI/SPI/EAC), cash flow, change orders | Daily |
| 7 | **Stakeholder Communication** | Auto-draft owner reports, RFI responses, sub notices | On-demand |
| 8 | **Workforce & Labor** | Crew productivity, labor forecasting, certification tracking | Daily |
| 9 | **Commissioning & Turnover** | IST sequencing, punch list intelligence, turnover tracking | Daily |
| 10 | **Environmental & Sustainability** | SWPPP compliance, LEED tracking, carbon footprint | Daily |
| 11 | **Claims & Dispute Prevention** | Contemporaneous records, delay analysis, notice tracking | Continuous |
| 12 | **Site Logistics** | Crane/hoist scheduling, material staging, headcount | Real-time |
| 13 | **Safety Compliance** | OSHA/MSHA/NIOSH regulatory compliance, stop-work authority | Continuous |

Plus a **rule-based Orchestrator** that coordinates cross-agent triggers, generates 6AM daily briefs, deduplicates alerts, and escalates critical events via SMS.

## Quick Start

```bash
# Install dependencies
uv sync

# Start infrastructure
docker compose up -d postgres redis

# Run database migrations
uv run alembic upgrade head

# Start the API server
uv run construction-pm

# In another terminal, start the frontend
cd frontend && npm install && npm run dev
```

The API is at `http://localhost:8000` (Swagger docs at `/docs`), and the dashboard at `http://localhost:3000`.

### Full Stack via Docker

```bash
docker compose up --build
```

This starts PostgreSQL + pgvector, Redis, the FastAPI backend, Celery worker + beat, and the Next.js frontend.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| AI Engine | Anthropic Claude API |
| Database | PostgreSQL 16 + pgvector (semantic search) |
| Cache/Messaging | Redis 7 (shared memory, pub/sub, alert dedup) |
| Task Scheduler | Celery + Redis broker |
| Frontend | Next.js 15 + TypeScript + Tailwind + Recharts |
| Simulation | NumPy + SciPy (Monte Carlo schedule analysis) |
| SMS Alerts | Twilio |
| Containerization | Docker Compose |

## Project Structure

```
src/
├── ai_agent/              # Core CLI agent (Calculator, CurrentTime, WebSearch)
└── construction/          # 13-agent construction PM ecosystem
    ├── agents/            # 13 agents + orchestrator + base class
    ├── tools/             # 23 tools (weather, OSHA, BIM, Monte Carlo, etc.)
    ├── schemas/           # 15 Pydantic schema modules
    ├── integrations/      # 13 external API clients (Procore, Autodesk, P6, etc.)
    ├── api/routers/       # 16 FastAPI routers
    ├── db/                # 27+ SQLAlchemy models, repositories, seed data
    ├── redis_/            # Client, pub/sub, shared memory
    └── tasks/             # Celery app + scheduled tasks

frontend/                  # Next.js 15 dashboard (15 pages, 11+ components)
tests/                     # 487 tests (agents, tools, API, integrations, E2E)
```

## Cross-Agent Intelligence

Agents communicate through Redis pub/sub and trigger each other automatically:

```
Supply Chain delay detected
  → Critical Path runs Monte Carlo simulation
  → Financial assesses cost impact
  → Claims logs contemporaneous record
  → Safety verifies replacement specs
  → Communication drafts owner update + sub notice
  → Orchestrator escalates via SMS if >$250k

Safety stop-work recommended
  → IMMEDIATE SMS to PM (highest priority)
  → Critical Path holds affected activities
  → Site Logistics restricts zone access
  → Claims logs safety event
  → Financial assesses stop-work cost
```

## Dashboard

15-page Next.js dashboard with real-time WebSocket updates:

- **Daily Brief** — Top 3 threats, 2 quality gaps, 1 acceleration opportunity
- **Risk Heat Map** — 5x5 probability/impact grid
- **Schedule** — Critical path Gantt + Monte Carlo results
- **Safety** — TRIR/DART gauges, OSHA 300 log, inspection readiness
- **Approvals** — One-click approve/reject with full transparency logs
- **Agent Monitor** — Status of all 13 agents with trigger buttons
- Plus pages for documents, compliance, supply chain, financial, workforce, commissioning, environmental, claims, and site logistics

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:
- `ANTHROPIC_API_KEY` — Claude API key (required)
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- API keys for Procore, Autodesk, Primavera, Portcast, Twilio, OpenWeatherMap, etc.

## Testing

```bash
# Run all 487 tests
uv run pytest

# By category
uv run pytest tests/construction/test_agents/       # Agent tests
uv run pytest tests/construction/test_tools/        # Tool tests
uv run pytest tests/construction/test_api/          # API router tests
uv run pytest tests/construction/test_integrations/ # Integration client tests
uv run pytest tests/construction/test_e2e_*.py      # E2E scenarios
```

E2E test scenarios:
- Transformer delay → full 13-agent cascade
- Safety stop-work → PM escalation
- Document contradiction → RFI flow
- OSHA inspection readiness check
- Daily brief generation

## CLI Agent

The original interactive CLI agent is still available:

```bash
uv run ai-agent
```

It provides Calculator, CurrentTime, and WebSearch tools in an interactive REPL.

## License

MIT
