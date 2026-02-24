#!/usr/bin/env python3
"""
Debug database connection and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.models import Base

def test_db():
    try:
        print("Testing database connection...")
        
        # Test basic connection
        engine = create_engine("postgresql://sentinel_user:strong_password@localhost:5432/sentinel")
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM tokens"))
            count = result.scalar()
            print(f"✅ Database connected successfully!")
            print(f"📊 Total tokens in database: {count}")
            
            # Check if sample data exists
            if count > 0:
                sample = conn.execute(text("SELECT address, name, risk_level FROM tokens LIMIT 3"))
                for row in sample:
                    print(f"   - {row.address[:8]}... | {row.name} | {row.risk_level}")
            else:
                print("⚠️  No tokens found - sample data may not be loaded")
                
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_api_endpoints():
    """Test if API endpoints are accessible"""
    import requests
    
    try:
        print("\nTesting API endpoints...")
        
        # Test health
        health = requests.get("http://localhost:8000/health", timeout=5)
        if health.status_code == 200:
            print("✅ Health endpoint accessible")
        else:
            print(f"❌ Health endpoint failed: {health.status_code}")
            
        # Test tokens endpoint
        tokens = requests.get("http://localhost:8000/api/v1/tokens", timeout=5)
        if tokens.status_code == 200:
            data = tokens.json()
            print(f"✅ Tokens endpoint accessible - found {data.get('total', 0)} tokens")
        else:
            print(f"❌ Tokens endpoint failed: {tokens.status_code}")
            print(f"   Response: {tokens.text[:200]}...")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    print("🔍 Sentinel Ledger - System Debug")
    print("=" * 50)
    
    # Test database
    db_ok = test_db()
    
    # Test API
    if db_ok:
        test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("Debug complete!")
