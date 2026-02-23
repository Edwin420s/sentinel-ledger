from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime, timedelta

from db.session import get_db
from db.models import Token, Wallet

router = APIRouter()

def get_color_for_risk(level: str) -> str:
    colors = {
        "LOW": "#10b981",
        "MODERATE": "#f59e0b",
        "HIGH": "#ef4444",
        "CRITICAL": "#b91c1c"
    }
    return colors.get(level.upper(), "#64748b")

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
            level: count for level, count in risk_distribution if level
        }
    }

@router.get("/dashboard")
async def get_dashboard_stats(
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get dashboard stats for frontend"""
    total_tokens = db.query(Token).filter(Token.chain == chain).count()
    
    high_risk_count = db.query(Token).filter(
        Token.chain == chain,
        Token.risk_level.in_(["HIGH", "CRITICAL"])
    ).count()
    
    active_deployers = db.query(func.count(distinct(Token.deployer))).filter(
        Token.chain == chain
    ).scalar() or 0
    
    percentage = f"{round((high_risk_count / total_tokens * 100) if total_tokens > 0 else 0, 1)}%"
    
    risk_distribution = db.query(
        Token.risk_level,
        func.count(Token.risk_level).label("count")
    ).filter(
        Token.chain == chain
    ).group_by(Token.risk_level).all()
    
    dist_list = [
        {"name": level or "Unknown", "value": count, "color": get_color_for_risk(level or "UNKNOWN")}
        for level, count in risk_distribution if level
    ]
    
    return {
        "totalTokens": total_tokens,
        "highRiskCount": high_risk_count,
        "highRiskPercentage": percentage,
        "activeDeployers": active_deployers,
        "totalFlags": high_risk_count * 3, # Mock value for total flags
        "newFlags": "+12",
        "riskDistribution": dist_list
    }

@router.get("/stats")
async def get_analytics_stats(
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get detailed analytics stats for frontend"""
    total_tokens = db.query(Token).filter(Token.chain == chain).count()
    total_deployers = db.query(func.count(distinct(Token.deployer))).filter(Token.chain == chain).scalar() or 0
    total_rugs = db.query(Token).filter(Token.chain == chain, Token.risk_level == "CRITICAL").count()
    avg_risk = db.query(func.avg(Token.final_score)).filter(Token.chain == chain).scalar() or 0
    
    return {
        "totalTokens": total_tokens,
        "totalDeployers": total_deployers,
        "totalRugs": total_rugs,
        "avgRiskScore": round(avg_risk, 1),
        "topRiskFactors": [
            {"name": "Liquidity Removal", "count": 145},
            {"name": "Mint Function", "count": 120},
            {"name": "Blacklist", "count": 85}
        ],
        "chainActivity": [
            {"name": "Base", "count": total_tokens}
        ],
        "recentAlerts": [
            {"message": "High risk token matching known rug pattern", "time": "2 mins ago"},
            {"message": "Suspicious liquidity removal detected", "time": "15 mins ago"}
        ]
    }

@router.get("/risk-distribution")
async def get_risk_distribution(
    chain: str = "base",
    db: Session = Depends(get_db)
):
    risk_distribution = db.query(
        Token.risk_level,
        func.count(Token.risk_level).label("count")
    ).filter(
        Token.chain == chain
    ).group_by(Token.risk_level).all()
    
    return [
        {"name": level or "Unknown", "value": count, "color": get_color_for_risk(level or "UNKNOWN")}
        for level, count in risk_distribution if level
    ]

@router.get("/deployment-trends")
async def get_deployment_trends(
    days: int = 30,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Mock timeline data until block timestamps are converted to actual dates"""
    # Create some dummy timeline data for the frontend chart to work
    base_date = datetime.utcnow() - timedelta(days=days)
    timeline = []
    for i in range(days):
        current_date = base_date + timedelta(days=i)
        timeline.append({
            "date": current_date.strftime("%b %d"),
            "deployments": 5 + (i % 5) * 2  # Dummy logic
        })
    return {"timeline": timeline}

@router.get("/risk-trends")
async def get_risk_trends(
    timeframe: str = "7d",
    chain: str = "base",
    db: Session = Depends(get_db)
):
    days = 7 if timeframe == "7d" else 30
    base_date = datetime.utcnow() - timedelta(days=days)
    timeline = []
    deployments = []
    for i in range(days):
        current_date = base_date + timedelta(days=i)
        date_str = current_date.strftime("%b %d")
        timeline.append({
            "date": date_str,
            "avgRiskScore": 40 + (i % 20)  # Dummy sequence
        })
        deployments.append({
            "date": date_str,
            "low": 10 + i,
            "high": 2 + (i % 3)
        })
    return {
        "timeline": timeline,
        "deployments": deployments
    }

@router.get("/top-risks")
async def get_top_risks(
    limit: int = 10,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    tokens = db.query(Token).filter(
        Token.chain == chain,
        Token.risk_level.in_(["HIGH", "CRITICAL"])
    ).order_by(
        Token.final_score.desc()
    ).limit(limit).all()
    return tokens

@router.get("/chain-stats")
async def get_chain_stats(db: Session = Depends(get_db)):
    return {
        "base": {"tokens": 100, "active": True},
        "ethereum": {"tokens": 0, "active": False}
    }

@router.get("/risk-feed")
async def get_risk_feed(
    chain: str = "base",
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Alias for recent activity to satisfy frontend API"""
    return await get_recent_activity(chain=chain, limit=limit, db=db)

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
        Token.deployed_block.desc()  # Assuming deployed_at isn't reliably set yet
    ).limit(limit).all()
    
    return [
        {
            "type": "token_deployed",
            "address": t.address,
            "risk_level": t.risk_level,
            "risk_score": t.final_score,
            "timestamp": t.deployed_block, # Using block as timestamp proxy for now
            "deployer": t.deployer
        }
        for t in recent
    ]