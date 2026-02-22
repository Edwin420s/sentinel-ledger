import logging
from typing import Optional
from datetime import datetime
from celery import Celery

from config.settings import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Celery app — used in production for async background tasks
# ---------------------------------------------------------------------------
celery_app = Celery(
    "sentinel",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


# ---------------------------------------------------------------------------
# Celery task (importable from anywhere without circular deps)
# ---------------------------------------------------------------------------
@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def analyze_token(self, token_address: str, chain: str):  # type: ignore[misc]
    """Celery task that orchestrates the full token analysis pipeline."""
    import asyncio
    try:
        asyncio.get_event_loop().run_until_complete(
            _run_analysis(token_address, chain)
        )
    except Exception as exc:
        logger.error(f"analyze_token task failed for {token_address}: {exc}")
        raise self.retry(exc=exc)


# Public shorthand used by contract_detector
trigger_token_analysis = analyze_token  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Shared async analysis implementation
# ---------------------------------------------------------------------------
async def _run_analysis(token_address: str, chain: str) -> None:
    """Full analysis pipeline for a single ERC-20 token."""
    from web3 import Web3
    from db.session import SessionLocal
    from db.models import Token
    from dex.liquidity_tracker import LiquidityTracker
    from intelligence.ownership_analyzer import OwnershipAnalyzer
    from intelligence.deployer_profiler import DeployerProfiler
    from risk.contract_risk import ContractRisk
    from risk.scoring_engine import ScoringEngine
    from ai.explanation_engine import ExplanationEngine

    logger.info(f"Starting analysis pipeline for {token_address} on {chain}")

    # Build Web3 connections
    rpc_url = settings.BASE_RPC_URL if chain == "base" else settings.ETH_RPC_URL
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # Optionally wire up cross-chain Ethereum web3
    w3_eth: Optional[Web3] = None
    if chain == "base" and settings.ETH_RPC_URL:
        w3_eth = Web3(Web3.HTTPProvider(settings.ETH_RPC_URL))

    db = SessionLocal()
    try:
        token = db.query(Token).filter(
            Token.address == token_address.lower(),
            Token.chain == chain,
        ).first()

        if not token:
            logger.warning(f"Token {token_address} not found in DB, skipping analysis")
            return

        deployer = token.deployer

        # ------------------------------------------------------------------
        # 1. Ownership / Contract Analysis
        # ------------------------------------------------------------------
        ownership_analyzer = OwnershipAnalyzer(w3, chain)
        ownership_result = await ownership_analyzer.analyze(token_address)
        ownership_score = ownership_result.get("ownership_score", 50)

        # ------------------------------------------------------------------
        # 2. Contract Risk (from ownership flags)
        # ------------------------------------------------------------------
        contract_flags = {
            "has_mint": "mint" in ownership_result.get("dangerous_functions", []),
            "mint_restricted": True,  # conservative default
            "has_blacklist": any(
                "blacklist" in f for f in ownership_result.get("dangerous_functions", [])
            ),
            "has_pause": any(
                "pause" in f for f in ownership_result.get("dangerous_functions", [])
            ),
            "can_change_fees": False,
            "is_proxy": False,
            "can_withdraw": "withdraw" in ownership_result.get("dangerous_functions", []),
        }
        contract_result = ContractRisk.calculate(contract_flags)
        contract_score = contract_result["score"]

        # ------------------------------------------------------------------
        # 3. Liquidity Intelligence
        # ------------------------------------------------------------------
        liquidity_tracker = LiquidityTracker(w3, chain)
        liquidity_result = await liquidity_tracker.track_token_liquidity(token_address)
        liquidity_score = liquidity_result.get("liquidity_score", 50)

        # ------------------------------------------------------------------
        # 4. Deployer Profiling (cross-chain if available)
        # ------------------------------------------------------------------
        deployer_profiler = DeployerProfiler(w3, w3_eth)
        deployer_result = await deployer_profiler.profile(deployer, chain)
        deployer_score = deployer_result.get("deployer_risk_score", 50)

        # ------------------------------------------------------------------
        # 5. Final Risk Score
        # ------------------------------------------------------------------
        scoring_engine = ScoringEngine()
        final_score, risk_level, breakdown = await scoring_engine.calculate_score(
            token_address=token_address,
            chain=chain,
            contract_score=contract_score,
            liquidity_score=liquidity_score,
            ownership_score=ownership_score,
            deployer_score=deployer_score,
        )

        # Collect all flags
        all_flags = (
            contract_result.get("flags", [])
            + ownership_result.get("flags", [])
            + liquidity_result.get("flags", [])
            + deployer_result.get("flags", [])
        )

        # ------------------------------------------------------------------
        # 6. AI Explanation
        # ------------------------------------------------------------------
        explanation_engine = ExplanationEngine()
        explanation = await explanation_engine.generate_explanation({
            "address": token_address,
            "chain": chain,
            "final_score": final_score,
            "risk_level": risk_level,
            "contract_score": contract_score,
            "liquidity_score": liquidity_score,
            "ownership_score": ownership_score,
            "deployer_score": deployer_score,
            "flags": all_flags,
            "deployer_total_tokens": deployer_result.get("total_tokens", 0),
            "deployer_rugs": deployer_result.get("suspected_rugs", 0),
            "wallet_age_days": deployer_result.get("wallet_age_days", 0),
        })

        # ------------------------------------------------------------------
        # 7. Persist flags + AI explanation back to token record
        # ------------------------------------------------------------------
        token.flags = all_flags
        if explanation:
            # Store explanation in flags for now (could add dedicated column)
            token.flags = all_flags + [f"AI: {explanation}"]
        token.analyzed_at = datetime.utcnow()
        db.commit()

        logger.info(
            f"Analysis complete for {token_address}: score={final_score:.1f}, level={risk_level}"
        )

    except Exception as e:
        logger.error(f"Analysis pipeline failed for {token_address}: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# ---------------------------------------------------------------------------
# JobRunner — used by the scheduler for batch analysis
# ---------------------------------------------------------------------------
class JobRunner:
    """Batch job runner for the analysis scheduler."""

    def __init__(self):
        self.use_celery = settings.ENV == "production"

    async def run_pending_analyses(self):
        """Pick up tokens that have not been analyzed yet and process them."""
        from db.session import SessionLocal
        from db.models import Token

        db = SessionLocal()
        try:
            pending = db.query(Token).filter(
                Token.analyzed_at.is_(None)
            ).limit(50).all()

            logger.info(f"Found {len(pending)} tokens pending analysis")

            for token in pending:
                if self.use_celery:
                    analyze_token.delay(token.address, token.chain)
                else:
                    await _run_analysis(token.address, token.chain)

        except Exception as e:
            logger.error(f"Error fetching pending analyses: {e}")
        finally:
            db.close()

    async def run_token_analysis(self, token_address: str, chain: str):
        """Trigger analysis for a single token directly."""
        if self.use_celery:
            analyze_token.delay(token_address, chain)
        else:
            await _run_analysis(token_address, chain)