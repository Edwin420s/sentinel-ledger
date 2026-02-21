import logging
from typing import Dict, Any, Tuple
from datetime import datetime

from config.settings import settings
from risk.risk_levels import classify_risk
from db.session import SessionLocal
from db.models import Token, RiskHistory

logger = logging.getLogger(__name__)

class ScoringEngine:
    def __init__(self):
        self.weights = {
            "contract": settings.CONTRACT_RISK_WEIGHT,
            "liquidity": settings.LIQUIDITY_RISK_WEIGHT,
            "ownership": settings.OWNERSHIP_RISK_WEIGHT,
            "deployer": settings.DEPLOYER_RISK_WEIGHT
        }
    
    async def calculate_score(self, token_address: str, chain: str,
                              contract_score: float,
                              liquidity_score: float,
                              ownership_score: float,
                              deployer_score: float) -> Tuple[float, str, Dict[str, Any]]:
        """Calculate final risk score"""
        
        # Ensure scores are within bounds
        contract_score = min(max(contract_score, 0), 100)
        liquidity_score = min(max(liquidity_score, 0), 100)
        ownership_score = min(max(ownership_score, 0), 100)
        deployer_score = min(max(deployer_score, 0), 100)
        
        # Calculate weighted score
        final_score = (
            contract_score * self.weights["contract"] +
            liquidity_score * self.weights["liquidity"] +
            ownership_score * self.weights["ownership"] +
            deployer_score * self.weights["deployer"]
        )
        
        # Determine risk level
        risk_level = classify_risk(final_score)
        
        # Create breakdown
        breakdown = {
            "contract": contract_score,
            "liquidity": liquidity_score,
            "ownership": ownership_score,
            "deployer": deployer_score,
            "final": final_score,
            "weights": self.weights
        }
        
        # Store in database
        await self._store_score(
            token_address=token_address,
            chain=chain,
            score=final_score,
            level=risk_level,
            breakdown=breakdown
        )
        
        return final_score, risk_level, breakdown
    
    async def _store_score(self, token_address: str, chain: str,
                           score: float, level: str, breakdown: Dict):
        """Store risk score in database"""
        db = SessionLocal()
        try:
            # Update token
            token = db.query(Token).filter(
                Token.address == token_address.lower(),
                Token.chain == chain
            ).first()
            
            if token:
                token.contract_score = breakdown.get("contract", 0)
                token.liquidity_score = breakdown.get("liquidity", 0)
                token.ownership_score = breakdown.get("ownership", 0)
                token.deployer_score = breakdown.get("deployer", 0)
                token.final_score = score
                token.risk_level = level
                token.analyzed_at = datetime.utcnow()
            
            # Create history entry
            history = RiskHistory(
                token_address=token_address.lower(),
                chain=chain,
                score=score,
                level=level,
                flags=breakdown
            )
            db.add(history)
            
            db.commit()
        except Exception as e:
            logger.error(f"Error storing risk score: {e}")
            db.rollback()
        finally:
            db.close()