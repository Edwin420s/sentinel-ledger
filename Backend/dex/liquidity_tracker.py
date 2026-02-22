import logging
from typing import Dict, Any, Optional
from datetime import datetime
from web3 import Web3

from db.session import SessionLocal
from db.models import LiquidityPool, Token
from dex.uniswap import UniswapTracker
from dex.aerodrome import AerodromeTracker
from config.chains import KNOWN_LP_LOCKERS, WETH_BASE, USDC_BASE

logger = logging.getLogger(__name__)

# Rough WETH/USDC price in USD — would be replaced by a price oracle in production
WETH_PRICE_USD = 2500.0
USDC_PRICE_USD = 1.0

STABLECOIN_ADDRS = {USDC_BASE.lower()}
WETH_ADDR = WETH_BASE.lower()


class LiquidityTracker:
    """Orchestrates liquidity pool detection across Uniswap V3 and Aerodrome on Base."""

    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.uniswap = UniswapTracker(w3, chain)
        self.aerodrome = AerodromeTracker(w3, chain)

    # ------------------------------------------------------------------
    # Entry point called by the analysis pipeline
    # ------------------------------------------------------------------
    async def track_token_liquidity(self, token_address: str) -> Dict[str, Any]:
        """
        Detect all DEX pools for a token, persist them to Postgres,
        and return a liquidity risk signal dict.
        """
        token_address = token_address.lower()
        all_pools: list[Dict[str, Any]] = []

        # Check Uniswap V3
        uni_pool = self.uniswap.detect_pool(token_address)
        if uni_pool:
            all_pools.append(uni_pool)

        # Check Aerodrome
        aero_pool = self.aerodrome.detect_pool(token_address)
        if aero_pool:
            all_pools.append(aero_pool)

        if not all_pools:
            logger.info(f"No DEX pools found for {token_address}")
            return {
                "has_liquidity": False,
                "liquidity_score": 20,
                "flags": ["No liquidity added"],
            }

        # Persist & enrich each pool record
        db = SessionLocal()
        try:
            token = db.query(Token).filter(
                Token.address == token_address, Token.chain == self.chain
            ).first()

            results = []
            for pool_data in all_pools:
                pool_record = self._upsert_pool(db, pool_data, token_address)
                liquidity_usd = self._estimate_liquidity_usd(pool_data)
                pool_record.current_liquidity_usd = liquidity_usd
                if pool_record.peak_liquidity_usd == 0 or liquidity_usd > pool_record.peak_liquidity_usd:
                    pool_record.peak_liquidity_usd = liquidity_usd
                if pool_record.initial_liquidity_usd == 0:
                    pool_record.initial_liquidity_usd = liquidity_usd
                    pool_record.first_liquidity_added_at = datetime.utcnow()

                results.append({
                    "pool_address": pool_data["address"],
                    "dex": pool_data["dex"],
                    "liquidity_usd": liquidity_usd,
                })

            db.commit()

            metrics = self._calculate_liquidity_metrics(results, token_address, db)
            return metrics

        except Exception as e:
            logger.error(f"Error tracking liquidity for {token_address}: {e}")
            db.rollback()
            return {"has_liquidity": True, "liquidity_score": 50, "flags": ["Liquidity analysis failed"]}
        finally:
            db.close()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _upsert_pool(self, db, pool_data: Dict[str, Any], token_address: str) -> LiquidityPool:
        pool_id = f"{self.chain}:{pool_data['address']}"
        record = db.query(LiquidityPool).filter(LiquidityPool.id == pool_id).first()
        if not record:
            record = LiquidityPool(
                id=pool_id,
                token_address=token_address,
                chain=self.chain,
                dex=pool_data["dex"],
                pool_address=pool_data["address"],
                created_at=datetime.utcnow(),
            )
            db.add(record)
        return record

    def _estimate_liquidity_usd(self, pool_data: Dict[str, Any]) -> float:
        """Rough USD estimate using reserve data from Aerodrome or raw liq from Uniswap."""
        try:
            paired = pool_data.get("paired_with", "").lower()
            if pool_data["dex"] == "aerodrome":
                reserve0 = pool_data.get("reserve0", 0)
                reserve1 = pool_data.get("reserve1", 0)
                # Determine which side is the pricing token
                t0 = pool_data.get("token0", "").lower()
                t1 = pool_data.get("token1", "").lower()
                if t0 == WETH_ADDR:
                    return (reserve0 / 1e18) * WETH_PRICE_USD * 2
                if t1 == WETH_ADDR:
                    return (reserve1 / 1e18) * WETH_PRICE_USD * 2
                if t0 in STABLECOIN_ADDRS:
                    return (reserve0 / 1e6) * 2
                if t1 in STABLECOIN_ADDRS:
                    return (reserve1 / 1e6) * 2
                return 0.0

            if pool_data["dex"] == "uniswap_v3":
                # Uni V3 raw "liquidity" is not in USD, just flag presence
                return 1.0 if pool_data.get("liquidity", 0) > 0 else 0.0

        except Exception as e:
            logger.debug(f"Could not estimate liquidity USD: {e}")
        return 0.0

    def _calculate_liquidity_metrics(
        self, result_pools: list, token_address: str, db
    ) -> Dict[str, Any]:
        """Derive a risk score and flags from the collected pool data."""
        score = 0
        flags = []

        total_liquidity_usd = sum(p["liquidity_usd"] for p in result_pools)
        has_meaningful = total_liquidity_usd > 0

        # Check locking — query DB pools to see lp_holder
        db_pools = db.query(LiquidityPool).filter(
            LiquidityPool.token_address == token_address,
            LiquidityPool.chain == self.chain,
        ).all()

        deployer_owns_lp = False
        liquidity_locked = False
        removed_early = False

        # Retrieve deployer address from token
        token = db.query(Token).filter(
            Token.address == token_address, Token.chain == self.chain
        ).first()
        deployer = token.deployer.lower() if token else None

        for pool in db_pools:
            lp_holder = (pool.lp_holder or "").lower()
            if lp_holder == deployer:
                deployer_owns_lp = True
            if lp_holder and lp_holder in [addr.lower() for addr in KNOWN_LP_LOCKERS]:
                liquidity_locked = True
                pool.liquidity_locked = True
            if pool.removed_early:
                removed_early = True

        # Low/no liquidity
        if not has_meaningful:
            score += 20
            flags.append("No liquidity added")
        elif total_liquidity_usd < 5000:
            score += 15
            flags.append(f"Low initial liquidity (<$5k): ~${total_liquidity_usd:.0f}")

        if not liquidity_locked:
            score += 30
            flags.append("Liquidity not locked")

        if deployer_owns_lp:
            score += 25
            flags.append("Deployer holds LP tokens")

        if removed_early:
            score += 40
            flags.append("Liquidity removed early")

        return {
            "has_liquidity": has_meaningful,
            "total_liquidity_usd": total_liquidity_usd,
            "liquidity_locked": liquidity_locked,
            "deployer_owns_lp": deployer_owns_lp,
            "removed_early": removed_early,
            "liquidity_score": min(score, 100),
            "flags": flags,
        }