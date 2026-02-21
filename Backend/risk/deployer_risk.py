from typing import Dict, Any, List

class DeployerRisk:
    @staticmethod
    def calculate(deployer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate deployer risk score"""
        score = 0
        flags = []
        
        # Deployment velocity
        total_tokens = deployer_data.get("total_tokens", 0)
        if total_tokens > 10:
            score += 15
            flags.append(f"High deployment velocity: {total_tokens} tokens")
        elif total_tokens > 5:
            score += 10
            flags.append(f"Moderate deployment velocity: {total_tokens} tokens")
        elif total_tokens > 2:
            score += 5
            flags.append(f"Multiple tokens: {total_tokens}")
        
        # Prior rugs
        suspected_rugs = deployer_data.get("suspected_rugs", 0)
        if suspected_rugs > 2:
            score += 40
            flags.append(f"Multiple suspected rugs: {suspected_rugs}")
        elif suspected_rugs > 0:
            score += 30
            flags.append(f"Prior suspected rug: {suspected_rugs}")
        
        # Wallet age
        age_days = deployer_data.get("wallet_age_days", 0)
        if age_days < 7:
            score += 20
            flags.append("Wallet age less than 7 days")
        elif age_days < 30:
            score += 10
            flags.append("Wallet age less than 30 days")
        
        # Cross-chain signals
        crosschain = deployer_data.get("crosschain", {})
        eth_data = crosschain.get("ethereum", {})
        if eth_data.get("suspected_rugs", 0) > 0:
            score += 30
            flags.append("Suspicious activity on Ethereum")
        
        # Cap score
        score = min(score, 100)
        
        return {
            "score": score,
            "flags": flags
        }