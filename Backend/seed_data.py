#!/usr/bin/env python3
"""
Seed sample data for testing Sentinel Ledger.
Run this after setting up the database.
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from db.session import engine, SessionLocal
from db.models import Token, Wallet, LiquidityPool, ContractAnalysis, RiskHistory

def create_sample_data():
    """Create sample tokens and wallets for testing."""
    
    db = SessionLocal()
    
    try:
        print("🌱 Seeding sample data...")
        
        # Sample deployer wallets
        sample_wallets = [
            {
                "address": "0x1234567890123456789012345678901234567890",
                "chain": "base",
                "total_contracts": 5,
                "erc20_count": 3,
                "suspected_rugs": 1,
                "deployer_risk_score": 45.0,
                "is_flagged": False,
                "wallet_age_days": 30
            },
            {
                "address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "chain": "base", 
                "total_contracts": 12,
                "erc20_count": 8,
                "suspected_rugs": 4,
                "deployer_risk_score": 78.0,
                "is_flagged": True,
                "wallet_age_days": 7
            },
            {
                "address": "0x9876543210987654321098765432109876543210",
                "chain": "base",
                "total_contracts": 2,
                "erc20_count": 1,
                "suspected_rugs": 0,
                "deployer_risk_score": 15.0,
                "is_flagged": False,
                "wallet_age_days": 90
            }
        ]
        
        # Create wallets
        for wallet_data in sample_wallets:
            wallet = Wallet(**wallet_data)
            db.add(wallet)
        
        db.commit()
        print(f"✅ Created {len(sample_wallets)} sample wallets")
        
        # Sample tokens
        sample_tokens = [
            {
                "address": "0xtoken1111111111111111111111111111111111111111",
                "chain": "base",
                "deployer": "0x1234567890123456789012345678901234567890",
                "deployed_block": 12345678,
                "name": "SafeToken",
                "symbol": "SAFE",
                "decimals": 18,
                "contract_score": 20.0,
                "liquidity_score": 15.0,
                "ownership_score": 25.0,
                "deployer_score": 45.0,
                "final_score": 28.5,
                "risk_level": "LOW",
                "flags": ["standard_erc20", "liquidity_locked"],
                "deployed_at": datetime.now() - timedelta(hours=2)
            },
            {
                "address": "0xtoken2222222222222222222222222222222222222222",
                "chain": "base",
                "deployer": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "deployed_block": 12345679,
                "name": "RiskyCoin",
                "symbol": "RISK",
                "decimals": 18,
                "contract_score": 85.0,
                "liquidity_score": 90.0,
                "ownership_score": 75.0,
                "deployer_score": 78.0,
                "final_score": 82.5,
                "risk_level": "HIGH",
                "flags": ["unlimited_mint", "owner_can_blacklist", "liquidity_unlockable"],
                "deployed_at": datetime.now() - timedelta(hours=6)
            },
            {
                "address": "0xtoken3333333333333333333333333333333333333333",
                "chain": "base",
                "deployer": "0x9876543210987654321098765432109876543210",
                "deployed_block": 12345680,
                "name": "MediumToken",
                "symbol": "MED",
                "decimals": 18,
                "contract_score": 50.0,
                "liquidity_score": 45.0,
                "ownership_score": 40.0,
                "deployer_score": 15.0,
                "final_score": 38.5,
                "risk_level": "MODERATE",
                "flags": ["upgradeable_proxy", "pause_function"],
                "deployed_at": datetime.now() - timedelta(hours=12)
            },
            {
                "address": "0xtoken4444444444444444444444444444444444444444",
                "chain": "base",
                "deployer": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "deployed_block": 12345681,
                "name": "CriticalRug",
                "symbol": "RUG",
                "decimals": 18,
                "contract_score": 95.0,
                "liquidity_score": 98.0,
                "ownership_score": 92.0,
                "deployer_score": 78.0,
                "final_score": 91.1,
                "risk_level": "CRITICAL",
                "flags": ["honeypot_pattern", "early_liquidity_removal", "deployer_flagged"],
                "deployed_at": datetime.now() - timedelta(hours=24)
            }
        ]
        
        # Create tokens
        for token_data in sample_tokens:
            token = Token(**token_data)
            db.add(token)
        
        db.commit()
        print(f"✅ Created {len(sample_tokens)} sample tokens")
        
        # Create some liquidity pools
        sample_pools = [
            {
                "id": "base:0xtoken1111111111111111111111111111111111111111",
                "token_address": "0xtoken1111111111111111111111111111111111111111",
                "chain": "base",
                "dex": "uniswap",
                "pool_address": "0xpool1111111111111111111111111111111111111111",
                "initial_liquidity_usd": 50000.0,
                "current_liquidity_usd": 48000.0,
                "peak_liquidity_usd": 52000.0,
                "liquidity_locked": True,
                "lp_holder": "0xlock1111111111111111111111111111111111111111",
                "created_at_block": 12345679,
                "created_at": datetime.now() - timedelta(hours=1, minutes=45),
                "first_liquidity_added_at": datetime.now() - timedelta(hours=1, minutes=45)
            },
            {
                "id": "base:0xtoken2222222222222222222222222222222222222222",
                "token_address": "0xtoken2222222222222222222222222222222222222222",
                "chain": "base",
                "dex": "aerodrome",
                "pool_address": "0xpool2222222222222222222222222222222222222222",
                "initial_liquidity_usd": 10000.0,
                "current_liquidity_usd": 500.0,
                "peak_liquidity_usd": 12000.0,
                "liquidity_locked": False,
                "lp_holder": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "created_at_block": 12345680,
                "created_at": datetime.now() - timedelta(hours=5, minutes=30),
                "first_liquidity_added_at": datetime.now() - timedelta(hours=5, minutes=30),
                "first_liquidity_removed_at": datetime.now() - timedelta(hours=3, minutes=15),
                "removed_early": True,
                "removal_percentage": 95.0
            }
        ]
        
        for pool_data in sample_pools:
            pool = LiquidityPool(**pool_data)
            db.add(pool)
        
        db.commit()
        print(f"✅ Created {len(sample_pools)} sample liquidity pools")
        
        # Create contract analysis
        sample_analysis = [
            {
                "token_address": "0xtoken1111111111111111111111111111111111111111",
                "chain": "base",
                "has_mint": True,
                "mint_restricted": True,
                "has_blacklist": False,
                "has_pause": False,
                "has_ownership": True,
                "ownership_renounced": True,
                "is_proxy": False,
                "upgradeable": False,
                "can_change_fees": False,
                "can_withdraw": False,
                "suspicious_patterns": [],
                "function_selectors": ["18160ddd", "70a08231", "a9059cbb", "095ea7b3"]
            },
            {
                "token_address": "0xtoken2222222222222222222222222222222222222222",
                "chain": "base",
                "has_mint": True,
                "mint_restricted": False,
                "has_blacklist": True,
                "has_pause": True,
                "has_ownership": True,
                "ownership_renounced": False,
                "is_proxy": True,
                "upgradeable": True,
                "can_change_fees": True,
                "can_withdraw": True,
                "suspicious_patterns": ["honeypot", "anti_whale"],
                "function_selectors": ["18160ddd", "70a08231", "a9059cbb", "095ea7b3", "40c10f19"]
            }
        ]
        
        for analysis_data in sample_analysis:
            analysis = ContractAnalysis(**analysis_data)
            db.add(analysis)
        
        db.commit()
        print(f"✅ Created {len(sample_analysis)} contract analyses")
        
        print("\n🎉 Sample data seeded successfully!")
        print("You can now start the API server and test the frontend.")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
