from typing import Dict, Any, List

class ContractRisk:
    @staticmethod
    def calculate(analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate contract risk score"""
        score = 0
        flags = []
        
        # Mint function
        if analysis.get("has_mint"):
            if not analysis.get("mint_restricted", True):
                score += 25
                flags.append("Public mint function")
            else:
                score += 15
                flags.append("Owner-only mint function")
        
        # Blacklist
        if analysis.get("has_blacklist"):
            score += 20
            flags.append("Has blacklist function")
        
        # Pause
        if analysis.get("has_pause"):
            score += 15
            flags.append("Can pause trading")
        
        # Fee changes
        if analysis.get("can_change_fees"):
            score += 10
            flags.append("Owner can change fees")
        
        # Proxy/upgradeable
        if analysis.get("is_proxy"):
            score += 15
            flags.append("Upgradeable proxy contract")
        
        # Withdraw function
        if analysis.get("can_withdraw"):
            score += 20
            flags.append("Owner can withdraw funds")
        
        # Cap score
        score = min(score, 100)
        
        return {
            "score": score,
            "flags": flags
        }