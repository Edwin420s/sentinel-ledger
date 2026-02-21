from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.session import get_db
from db.models import Token

router = APIRouter()

@router.get("/summary")
async def get_summary(
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get platform summary statistics"""
    total_tokens = db.query(Token).filter(Token.chain == chain).count()
    
    risk_distribution = db.query(
        Token.risk_level,
        func.count(Token.risk_level).label("count")
    ).filter(
        Token.chain == chain
    ).group_by(Token.risk_level).all()
    
    avg_risk = db.query(
        func.avg(Token.final_score)
    ).filter(Token.chain == chain).scalar() or 0
    
    return {
        "chain": chain,
        "total_tokens": total_tokens,
        "average_risk": round(avg_risk, 2),
        "risk_distribution": {
            level: count for level, count in risk_distribution
        }
    }

@router.get("/recent-activity")
async def get_recent_activity(
    chain: str = "base",
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get recent activity feed"""
    recent = db.query(Token).filter(
        Token.chain == chain
    ).order_by(
        Token.deployed_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "type": "token_deployed",
            "address": t.address,
            "risk_level": t.risk_level,
            "risk_score": t.final_score,
            "timestamp": t.deployed_at,
            "deployer": t.deployer
        }
        for t in recent
    ]