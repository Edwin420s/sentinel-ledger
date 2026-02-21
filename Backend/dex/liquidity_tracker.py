import logging
from typing import Dict, Any, Optional, List
from web3 import Web3
from datetime import datetime, timedelta

from dex.uniswap import UniswapTracker
from dex.aerodrome import AerodromeTracker
from db.session import SessionLocal
from db.models import LiquidityPool, Token

logger = logging.getLogger(__name__)

class LiquidityTracker:
    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.uniswap = UniswapTracker(w3, chain)
        self.aerodrome = AerodromeTracker(w3, chain)
    
    async def track_token_liquidity(self, token_address: str) -> Dict[str, Any]:
        """Track liquidity for a token across all DEXes"""
        token_address = token_address.lower()
        
        # Check all DEXes for pools
        pools = []
        
        # Uniswap
        uniswap_pool = self.uniswap.detect_pool(token_address)
        if uniswap_pool:
            pools.append(uniswap_pool)
        
        # Aerodrome
        aerodrome_pool = self.aerodrome.detect_pool(token_address)
        if aerodrome_pool:
            pools.append(aerodrome_pool)
        
        if not pools:
            return {
                "has_liquidity": False,
                "liquidity_score": 20,  # No liquidity is risky
                "pools": []
            }
        
        # Store pools in database
        await self._store_pools(token_address, pools)
        
        # Calculate liquidity metrics
        liquidity_data = await self._calculate_liquidity_metrics(token_address, pools)
        
        return liquidity_data
    
    async def _store_pools(self, token_address: str, pools: List[Dict]):
        """Store pool information in database"""
        db = SessionLocal()
        try:
            for pool in pools:
                existing = db.query(LiquidityPool).filter(
                    LiquidityPool.id == f"{self.chain}:{pool['address']}"
                ).first()
                
                if not existing:
                    pool_record = LiquidityPool(
                        id=f"{self.chain}:{pool['address']}",
                        token_address=token_address,
                        chain=self.chain,
                        dex=pool["dex"],
                        pool_address=pool["address"].lower(),
                        created_at_block=pool.get("created_at_block"),
                        created_at=datetime.utcnow()
                    )
                    db.add(pool_record)
            
            db.commit()
        except Exception as e:
            logger.error(f"Error storing pools: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _calculate_liquidity_metrics(self, token_address: str, pools: List[Dict]) -> Dict[str, Any]:
        """Calculate liquidity risk metrics"""
        db = SessionLocal()
        try:
            # Get token info
            token = db.query(Token).filter(
                Token.address == token_address,
                Token.chain == self.chain
            ).first()
            
            if not token:
                return {"liquidity_score": 50, "flags": []}
            
            # Calculate liquidity score
            score = 0
            flags = []
            
            # Check if any liquidity exists
            if not pools:
                score += 20
                flags.append("No liquidity pools detected")
            
            # Check liquidity lock status (simplified)
            liquidity_locked = False
            lp_holder = None
            
            # In production, would check if LP tokens are locked
            # For now, assume not locked
            if not liquidity_locked:
                score += 30
                flags.append("Liquidity not locked")
            
            # Check deployer LP ownership
            # Would check if deployer holds LP tokens
            deployer_owns_lp = False
            if deployer_owns_lp:
                score += 25
                flags.append("Deployer holds LP tokens")
            
            # Check initial liquidity amount
            # Would need to calculate USD value
            low_liquidity = True  # Placeholder
            if low_liquidity:
                score += 15
                flags.append("Low initial liquidity")
            
            # Cap score at 100
            score = min(score, 100)
            
            return {
                "liquidity_score": score,
                "flags": flags,
                "pools": pools,
                "has_liquidity": len(pools) > 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating liquidity metrics: {e}")
            return {"liquidity_score": 50, "flags": ["Error calculating liquidity"]}
        finally:
            db.close()
    
    async def monitor_liquidity_changes(self, token_address: str):
        """Monitor for liquidity changes in the first 6 hours"""
        # This would be called by a scheduled task
        # Would check for:
        # - Liquidity additions
        # - Liquidity removals
        # - LP token burns
        pass