import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.routes import tokens, wallets, analytics

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sentinel Ledger API",
    description="Cross-chain risk intelligence infrastructure for Base and Ethereum",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ---------------------------------------------------------------------------
# Lifecycle events
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """Verify DB connectivity on startup."""
    import sqlalchemy
    from db.session import engine
    try:
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        logger.info("Database connection OK")
    except Exception as e:
        logger.error(f"Database connection failed on startup: {e}")
    logger.info("Sentinel Ledger API started")


@app.on_event("shutdown")
async def shutdown_event():
    from db.session import engine
    engine.dispose()
    logger.info("Sentinel Ledger API shut down")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(tokens.router, prefix="/api/v1/tokens", tags=["tokens"])
app.include_router(wallets.router, prefix="/api/v1/wallets", tags=["wallets"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

# ---------------------------------------------------------------------------
# Root endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["meta"])
async def root():
    return {
        "service": "Sentinel Ledger",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health", tags=["meta"])
async def health_check():
    """Health check endpoint for load balancers and uptime monitoring."""
    from db.session import engine
    db_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "unavailable",
    }