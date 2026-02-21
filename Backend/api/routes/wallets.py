from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import Wallet, Token
from api.schemas import WalletResponse, WalletDetailResponse

router = APIRouter()

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