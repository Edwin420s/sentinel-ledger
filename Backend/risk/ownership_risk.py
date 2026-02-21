from typing import Dict, Any, List

class OwnershipRisk:
    @staticmethod
    def calculate(ownership_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ownership risk score"""
        score = 0
        flags = []
        
        # Ownership not renounced
        if ownership_data.get("has_ownership") and not ownership_data.get("ownership_renounced"):
            score += 30
            flags.append("Ownership not renounced")
        
        # Can transfer ownership
        if ownership_data.get("can_transfer_ownership"):
            score += 20
            flags.append("Ownership can be transferred")
        
        # Dangerous functions present
        dangerous = ownership_data.get("dangerous_functions", [])
        if "mint" in dangerous:
            score += 25
            flags.append("Has mint function")
        if "blacklist" in str(dangerous):
            score += 20
            flags.append("Has blacklist function")
        if "pause" in str(dangerous):
            score += 15
            flags.append("Can pause trading")
        if "withdraw" in dangerous:
            score += 20
            flags.append("Owner can withdraw funds")
        
        # Cap score
        score = min(score, 100)
        
        return {
            "score": score,
            "flags": flags
        }