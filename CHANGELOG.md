# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-02-07

### Added

#### Core
- `system_prompt` parameter on `Agent.__init__()` for specialized agent personas
- `ConstructionSettings` config with 35+ environment variables
- `construction-pm` CLI entrypoint for FastAPI server

#### 13 Construction Agents
- **Tier 1 (Core):** Risk Forecaster (hourly), Document Intelligence (on-demand),
  Critical Path Optimizer (on-demand), Compliance Verifier (twice daily),
  Supply Chain Resilience (every 4h)
- **Tier 2 (Extended):** Financial Intelligence (daily),
  Stakeholder Communication (on-demand), Workforce & Labor (daily)
- **Tier 3 (Advanced):** Commissioning & Turnover (daily),
  Environmental & Sustainability (daily), Claims & Dispute Prevention (continuous),
  Site Logistics (real-time), Safety Compliance — OSHA/MSHA/NIOSH (continuous)
- Rule-based Orchestrator with cross-agent triggering, daily brief generation,
  SMS escalation (>$250k or safety-critical), and hash-based alert deduplication

#### 23 Tools
- Weather forecast, OSHA search, risk database, supply chain monitor,
  schedule query, Monte Carlo simulation (NumPy/SciPy), BIM query,
  compliance database, document search, notifications (Twilio SMS),
  financial query, workforce query, draft communication,
  commissioning query, environmental query, claims query, site logistics query,
  OSHA compliance, MSHA compliance, NIOSH lookup, safety metrics,
  hazard analysis, training tracker

#### 15 Pydantic Schema Modules
- common, risk, supply_chain, schedule, compliance, document, financial,
  workforce, communication, commissioning, environmental, claims,
  site_logistics, safety, orchestrator

#### 13 Integration Clients
- Procore (OAuth 2.0), Autodesk ACC/BIM 360 (OAuth 2.0),
  Primavera P6, MS Project, Portcast, Vizion, Terminal49,
  Twilio, OpenWeatherMap, OSHA API, MSHA API, NIOSH API
- `BaseAsyncClient` with exponential backoff retry, rate limiting, auth

#### FastAPI Backend
- 16 API routers: risks, documents, schedule, compliance, supply-chain,
  financial, workforce, commissioning, environmental, claims, site-logistics,
  safety, briefs, approvals, agents, WebSocket
- WebSocket `/ws/dashboard` for real-time updates
- CORS middleware for frontend integration

#### Database
- 27+ SQLAlchemy ORM models with PostgreSQL + pgvector
- Async engine with `asyncpg`
- Repository pattern for data access (Risk, Document, Schedule,
  Compliance, Vendor, Approval, DailyBrief, Safety)
- Alembic async migration setup
- Comprehensive seed data with transformer delay scenario

#### Redis
- Connection pool management
- Pub/sub for inter-agent communication (9 channels)
- Typed shared memory for agent state, risks, vendor alerts,
  budget status, safety readiness, alert deduplication

#### Celery
- Scheduled tasks for all 13 agents with appropriate intervals
- 6AM daily brief generation via crontab
- Redis broker configuration

#### Next.js 15 Frontend
- 15 dashboard pages (Dashboard, Risks, Schedule, Documents, Compliance,
  Supply Chain, Financial, Workforce, Commissioning, Environmental,
  Claims, Site Logistics, Safety, Approvals, Agents)
- 11 dashboard components (DailyBriefCard, RiskHeatMap, CriticalPathGantt,
  EarnedValueChart, SafetyDashboard, OSHA300Table, and more)
- Layout with sidebar navigation, header, alert banner
- WebSocket hook for live updates
- TypeScript API client matching all backend endpoints

#### Infrastructure
- Docker Compose with PostgreSQL+pgvector, Redis, backend, Celery
  worker/beat, frontend
- `Dockerfile.backend` and `Dockerfile.frontend`

#### Testing
- 487 tests (79 test files) covering agents, tools, API, integrations, orchestrator
- E2E tests: transformer delay cascade, safety stop-work escalation,
  document contradiction → RFI flow, OSHA inspection readiness
- Shared pytest fixtures in `conftest.py`

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
