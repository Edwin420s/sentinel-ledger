import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from web3 import Web3

from db.session import SessionLocal
from db.models import Wallet, Token
from intelligence.crosschain_analyzer import CrossChainAnalyzer

logger = logging.getLogger(__name__)

class DeployerProfiler:
    def __init__(self, w3_base: Web3, w3_eth: Optional[Web3] = None):
        self.w3_base = w3_base
        self.w3_eth = w3_eth
        self.crosschain = CrossChainAnalyzer(w3_base, w3_eth) if w3_eth else None
    
    async def profile(self, deployer_address: str, chain: str = "base") -> Dict[str, Any]:
        """Profile a deployer wallet"""
        deployer_address = deployer_address.lower()
        
        db = SessionLocal()
        try:
            # Get or create wallet record
            wallet = db.query(Wallet).filter(
                Wallet.address == deployer_address,
                Wallet.chain == chain
            ).first()
            
            if not wallet:
                wallet = Wallet(
                    address=deployer_address,
                    chain=chain,
                    first_seen_at=datetime.utcnow()
                )
                db.add(wallet)
                db.commit()
            
            # Get all tokens deployed by this wallet
            deployed_tokens = db.query(Token).filter(
                Token.deployer == deployer_address,
                Token.chain == chain
            ).all()
            
            # Calculate metrics
            total_tokens = len(deployed_tokens)
            erc20_count = total_tokens  # We only track ERC20s
            
            # Calculate suspected rugs
            suspected_rugs = 0
            for token in deployed_tokens:
                if token.liquidity_score and token.liquidity_score > 70:
                    suspected_rugs += 1
            
            # Calculate wallet age
            if wallet.first_seen_at:
                age_days = (datetime.utcnow() - wallet.first_seen_at).days
            else:
                age_days = 0
            
            # Get cross-chain data if available
            crosschain_data = {}
            if self.crosschain and chain == "base":
                crosschain_data = await self.crosschain.analyze_wallet(deployer_address)
            
            # Calculate deployer risk score
            score = self._calculate_deployer_risk(
                total_tokens=total_tokens,
                suspected_rugs=suspected_rugs,
                age_days=age_days,
                crosschain_data=crosschain_data
            )
            
            # Update wallet
            wallet.total_contracts = total_tokens
            wallet.erc20_count = erc20_count
            wallet.suspected_rugs = suspected_rugs
            wallet.wallet_age_days = age_days
            wallet.deployer_risk_score = score["score"]
            wallet.flags = score["flags"]
            
            if crosschain_data:
                wallet.ethereum_activity = crosschain_data.get("ethereum", {})
            
            db.commit()
            
            return {
                "address": deployer_address,
                "total_tokens": total_tokens,
                "suspected_rugs": suspected_rugs,
                "wallet_age_days": age_days,
                "deployer_risk_score": score["score"],
                "flags": score["flags"],
                "crosschain": crosschain_data
            }
            
        except Exception as e:
            logger.error(f"Error profiling deployer {deployer_address}: {e}")
            return {
                "address": deployer_address,
                "error": str(e),
                "deployer_risk_score": 50
            }
        finally:
            db.close()
    
    def _calculate_deployer_risk(self, total_tokens: int, suspected_rugs: int,
                                  age_days: int, crosschain_data: Dict) -> Dict[str, Any]:
        """Calculate deployer risk score"""
        score = 0
        flags = []
        
        # Deployment velocity
        if total_tokens > 10:
            score += 15
            flags.append(f"High deployment velocity: {total_tokens} tokens")
        elif total_tokens > 5:
            score += 10
            flags.append(f"Moderate deployment velocity: {total_tokens} tokens")
        elif total_tokens > 2:
            score += 5
            flags.append(f"Multiple tokens: {total_tokens}")
        
        # Repeat rug patterns
        if suspected_rugs > 2:
            score += 40
            flags.append(f"Multiple suspected rugs: {suspected_rugs}")
        elif suspected_rugs > 0:
            score += 30
            flags.append(f"Prior suspected rug: {suspected_rugs}")
        
        # Wallet age
        if age_days < 7:
            score += 20
            flags.append("Wallet age less than 7 days")
        elif age_days < 30:
            score += 10
            flags.append("Wallet age less than 30 days")
        
        # Cross-chain signals
        if crosschain_data:
            eth_data = crosschain_data.get("ethereum", {})
            if eth_data.get("suspected_rugs", 0) > 0:
                score += 30
                flags.append("Suspicious activity on Ethereum")
            
            if eth_data.get("funded_by_flagged_wallet", False):
                score += 20
                flags.append("Funded by flagged wallet")
        
        # Cap score
        score = min(score, 100)
        
        return {
            "score": score,
            "flags": flags
        }