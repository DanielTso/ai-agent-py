"""FastAPI application for Construction PM AI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB pool, Redis connection
    yield
    # Shutdown: close connections


def create_app() -> FastAPI:
    app = FastAPI(
        title="Construction PM AI",
        description=(
            "13-Agent Construction Project Management"
            " AI Ecosystem"
        ),
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Include all routers
    from construction.api.routers import (
        agents,
        approvals,
        briefs,
        claims,
        commissioning,
        compliance,
        documents,
        environmental,
        financial,
        risks,
        safety,
        schedule,
        site_logistics,
        supply_chain,
        workforce,
        ws,
    )

    app.include_router(
        risks.router, prefix="/api/risks", tags=["risks"],
    )
    app.include_router(
        documents.router,
        prefix="/api/documents",
        tags=["documents"],
    )
    app.include_router(
        schedule.router,
        prefix="/api/schedule",
        tags=["schedule"],
    )
    app.include_router(
        compliance.router,
        prefix="/api/compliance",
        tags=["compliance"],
    )
    app.include_router(
        supply_chain.router,
        prefix="/api/supply-chain",
        tags=["supply-chain"],
    )
    app.include_router(
        financial.router,
        prefix="/api/financial",
        tags=["financial"],
    )
    app.include_router(
        workforce.router,
        prefix="/api/workforce",
        tags=["workforce"],
    )
    app.include_router(
        commissioning.router,
        prefix="/api/commissioning",
        tags=["commissioning"],
    )
    app.include_router(
        environmental.router,
        prefix="/api/environmental",
        tags=["environmental"],
    )
    app.include_router(
        claims.router,
        prefix="/api/claims",
        tags=["claims"],
    )
    app.include_router(
        site_logistics.router,
        prefix="/api/site-logistics",
        tags=["site-logistics"],
    )
    app.include_router(
        safety.router,
        prefix="/api/safety",
        tags=["safety"],
    )
    app.include_router(
        briefs.router,
        prefix="/api/briefs",
        tags=["briefs"],
    )
    app.include_router(
        approvals.router,
        prefix="/api/approvals",
        tags=["approvals"],
    )
    app.include_router(
        agents.router,
        prefix="/api/agents",
        tags=["agents"],
    )
    app.include_router(ws.router, tags=["websocket"])

    @app.get("/api/health")
    async def health():
        return {"status": "healthy", "version": "0.1.0"}

    return app


app = create_app()


def run_server():
    import uvicorn

    uvicorn.run(
        "construction.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
