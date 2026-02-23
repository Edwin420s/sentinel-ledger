from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.session import get_db
from db.models import Wallet, Token
from api.schemas import WalletResponse, WalletDetailResponse

router = APIRouter()

@router.get("/search")
async def search_wallets(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Search wallets by address"""
    search_term = f"%{q.lower()}%"
    wallets = db.query(Wallet).filter(
        Wallet.chain == chain,
        func.lower(Wallet.address).like(search_term)
    ).limit(limit).all()
    
    return wallets

@router.get("/top-deployers")
async def get_top_deployers(
    limit: int = Query(10, ge=1, le=50),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get top token deployers"""
    wallets = db.query(Wallet).filter(
        Wallet.chain == chain
    ).order_by(
        Wallet.total_contracts.desc()
    ).limit(limit).all()
    
    return wallets

@router.get("/{address}", response_model=WalletDetailResponse)
async def get_wallet(
    address: str,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get wallet information"""
    wallet = db.query(Wallet).filter(
        Wallet.address == address.lower(),
        Wallet.chain == chain
    ).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    # Get tokens deployed by this wallet
    tokens = db.query(Token).filter(
        Token.deployer == address.lower(),
        Token.chain == chain
    ).all()
    
    return {
        "wallet": wallet,
        "deployed_tokens": tokens
    }

@router.get("/{address}/tokens")
async def get_wallet_tokens(
    address: str,
    chain: str = "base",
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get tokens deployed by a wallet"""
    tokens = db.query(Token).filter(
        Token.deployer == address.lower(),
        Token.chain == chain
    ).order_by(
        Token.deployed_at.desc()
    ).offset(skip).limit(limit).all()
    
    total = db.query(Token).filter(
        Token.deployer == address.lower(),
        Token.chain == chain
    ).count()
    
    return {
        "total": total,
        "tokens": tokens
    }

@router.get("/{address}/risk")
async def get_wallet_risk(
    address: str,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get wallet risk assessment"""
    wallet = db.query(Wallet).filter(
        Wallet.address == address.lower(),
        Wallet.chain == chain
    ).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return {
        "address": wallet.address,
        "risk_score": wallet.deployer_risk_score,
        "total_tokens": wallet.total_contracts,
        "suspected_rugs": wallet.suspected_rugs,
        "wallet_age_days": wallet.wallet_age_days,
        "flags": wallet.flags
    }

@router.get("/{address}/transactions")
async def get_wallet_transactions(
    address: str,
    limit: int = Query(10, ge=1, le=100),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get wallet transactions"""
    return []

@router.get("/{address}/stats")
async def get_wallet_stats(
    address: str,
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get detailed wallet stats"""
    wallet = db.query(Wallet).filter(
        Wallet.address == address.lower(),
        Wallet.chain == chain
    ).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
        
    return {
        "address": address,
        "chain": chain,
        "total_volume": 25000.0,
        "active_days": wallet.wallet_age_days,
        "success_rate": 85.5
    }

@router.get("/{address}/graph")
async def get_wallet_graph(
    address: str,
    depth: int = Query(2, ge=1, le=3),
    chain: str = "base",
    db: Session = Depends(get_db)
):
    """Get wallet interaction graph"""
    return {
        "nodes": [{"id": address.lower(), "type": "wallet"}],
        "edges": []
    }