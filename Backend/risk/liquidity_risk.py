from typing import Dict, Any, List

class LiquidityRisk:
    @staticmethod
    def calculate(liquidity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate liquidity risk score"""
        score = 0
        flags = []
        
        # No liquidity
        if not liquidity_data.get("has_liquidity", False):
            score += 20
            flags.append("No liquidity added")
        
        # Liquidity not locked
        if not liquidity_data.get("liquidity_locked", True):
            score += 30
            flags.append("Liquidity not locked")
        
        # Deployer owns LP
        if liquidity_data.get("deployer_owns_lp", False):
            score += 25
            flags.append("Deployer holds LP tokens")
        
        # Early removal detected
        if liquidity_data.get("removed_early", False):
            score += 40
            flags.append("Liquidity removed early")
        
        # Low initial liquidity
        initial_liquidity = liquidity_data.get("initial_liquidity_usd", 0)
        if 0 < initial_liquidity < 5000:
            score += 15
            flags.append("Low initial liquidity (<$5k)")
        
        # Cap score
        score = min(score, 100)
        
        return {
            "score": score,
            "flags": flags
        }