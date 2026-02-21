from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TokenBase(BaseModel):
    address: str
    chain: str
    deployer: str
    risk_level: str
    final_score: float

class TokenResponse(TokenBase):
    deployed_at: datetime
    contract_score: float
    liquidity_score: float
    ownership_score: float
    deployer_score: float
    
    class Config:
        orm_mode = True

class TokenDetailResponse(TokenResponse):
    flags: List[str] = []
    liquidity_pools: List[Dict[str, Any]] = []
    risk_history: List[Dict[str, Any]] = []
    
    class Config:
        orm_mode = True

class TokenListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    tokens: List[TokenResponse]

class WalletBase(BaseModel):
    address: str
    chain: str
    total_contracts: int
    suspected_rugs: int
    deployer_risk_score: float

class WalletResponse(WalletBase):
    first_seen_at: Optional[datetime]
    wallet_age_days: int
    flags: List[str] = []
    
    class Config:
        orm_mode = True

class WalletDetailResponse(BaseModel):
    wallet: WalletResponse
    deployed_tokens: List[TokenResponse]

class RiskBreakdown(BaseModel):
    contract: float
    liquidity: float
    ownership: float
    deployer: float
    final: float
    weights: Dict[str, float]