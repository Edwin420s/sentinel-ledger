from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.session import get_db
from db.models import Token
from api.schemas import TokenResponse, TokenDetailResponse, TokenListResponse

router = APIRouter()

@router.get("/", response_model=TokenListResponse)
async def list_tokens(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    risk_level: Optional[str] = None,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """List tokens with optional filtering"""
    query = db.query(Token).filter(Token.chain == chain)
    
    if risk_level:
        query = query.filter(Token.risk_level == risk_level.upper())
    
    total = query.count()
    tokens = query.order_by(Token.deployed_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "tokens": tokens
    }

@router.get("/recent", response_model=List[TokenResponse])
async def recent_tokens(
    limit: int = Query(20, ge=1, le=50),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get most recently deployed tokens"""
    tokens = db.query(Token).filter(
        Token.chain == chain
    ).order_by(
        Token.deployed_at.desc()
    ).limit(limit).all()
    
    return tokens

@router.get("/high-risk", response_model=List[TokenResponse])
async def high_risk_tokens(
    limit: int = Query(20, ge=1, le=50),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get highest risk tokens"""
    tokens = db.query(Token).filter(
        Token.chain == chain,
        Token.risk_level.in_(["HIGH", "CRITICAL"])
    ).order_by(
        Token.final_score.desc()
    ).limit(limit).all()
    
    return tokens

@router.get("/{address}", response_model=TokenDetailResponse)
async def get_token(
    address: str,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get detailed token information"""
    token = db.query(Token).filter(
        Token.address == address.lower(),
        Token.chain == chain
    ).first()
    
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    return token

@router.get("/search", response_model=TokenListResponse)
async def search_tokens(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Search tokens by name, symbol, or address"""
    search_term = f"%{q.lower()}%"
    query = db.query(Token).filter(
        Token.chain == chain,
        (func.lower(Token.address).like(search_term)) | 
        (func.lower(Token.name).like(search_term)) | 
        (func.lower(Token.symbol).like(search_term))
    )
    
    total = query.count()
    tokens = query.order_by(Token.deployed_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "tokens": tokens
    }

@router.get("/{address}/stats")
async def get_token_stats(
    address: str,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get token statistics"""
    token = db.query(Token).filter(Token.address == address.lower(), Token.chain == chain).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
        
    return {
        "address": address,
        "chain": chain,
        "liquidity": 10000.0,
        "volume24h": 5000.0,
        "transactions24h": 150,
        "holders": 42
    }

@router.get("/{address}/transactions")
async def get_token_transactions(
    address: str,
    limit: int = Query(20, ge=1, le=100),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    # Dummy implementation since we don't store individual transactions yet
    return []

@router.get("/{address}/holders")
async def get_token_holders(
    address: str,
    limit: int = Query(10, ge=1, le=100),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    # Dummy implementation since we don't store holders yet
    return []

@router.post("/compare")
async def compare_tokens(
    addresses: List[str] = Body(..., embed=True),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Compare multiple tokens"""
    tokens = db.query(Token).filter(
        Token.address.in_([a.lower() for a in addresses]),
        Token.chain == chain
    ).all()
    
    return tokens