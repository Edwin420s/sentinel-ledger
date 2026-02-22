"""
Sentinel Ledger — Indexer Entry Point

Usage:
    python -m indexer.run

Starts both the Base and Ethereum block listeners concurrently,
plus the background task scheduler for pending token analyses.
"""
import asyncio
import logging
import signal
import sys

from config.settings import settings
from indexer.base_listener import BaseListener
from indexer.ethereum_listener import EthereumListener
from tasks.scheduler import Scheduler
from tasks.job_runner import JobRunner
from db.session import engine
from db.models import Base

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("indexer.run")


# ---------------------------------------------------------------------------
# DB initialisation (create tables if they don't exist)
# ---------------------------------------------------------------------------
def init_db() -> None:
    logger.info("Ensuring database tables exist…")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main() -> None:
    init_db()

    base_listener = BaseListener()
    eth_listener = EthereumListener()
    job_runner = JobRunner()
    scheduler = Scheduler()

    # Register recurring jobs
    scheduler.add_job(
        name="pending_token_analyses",
        interval_seconds=settings.BATCH_INTERVAL_SECONDS,
        func=job_runner.run_pending_analyses,
    )

    # Graceful shutdown handler
    loop = asyncio.get_running_loop()

    def _handle_signal():
        logger.info("Shutdown signal received, stopping listeners…")
        base_listener.stop()
        eth_listener.stop()
        scheduler.stop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _handle_signal)

    logger.info("Starting Sentinel Ledger indexer…")

    await asyncio.gather(
        base_listener.run(),
        eth_listener.run(),
        scheduler.run_forever(),
    )


if __name__ == "__main__":
    asyncio.run(main())
