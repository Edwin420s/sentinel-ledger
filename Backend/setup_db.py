#!/usr/bin/env python3
"""
Simple database setup script to create basic tables
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sentinel_user:strong_password@localhost:5432/sentinel")

def create_tables():
    """Create basic tables for the application"""
    engine = create_engine(DATABASE_URL)
    
    # Basic tokens table
    tokens_sql = """
    CREATE TABLE IF NOT EXISTS tokens (
        address VARCHAR(42) PRIMARY KEY,
        chain VARCHAR(50) NOT NULL,
        deployer VARCHAR(42),
        deployer_original_chain VARCHAR(50),
        deployed_block BIGINT,
        deployed_at TIMESTAMP,
        bytecode_hash VARCHAR(66),
        name TEXT,
        symbol TEXT,
        decimals INTEGER,
        contract_score DECIMAL(5,4),
        liquidity_score DECIMAL(5,4),
        ownership_score DECIMAL(5,4),
        deployer_score DECIMAL(5,4),
        final_score DECIMAL(5,4),
        risk_level VARCHAR(20),
        flags TEXT,
        analyzed_at TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Basic wallets table
    wallets_sql = """
    CREATE TABLE IF NOT EXISTS wallets (
        address VARCHAR(42) PRIMARY KEY,
        first_seen TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        transaction_count INTEGER DEFAULT 0,
        total_value_eth DECIMAL(20,8),
        risk_score DECIMAL(5,4),
        flags TEXT
    );
    """
    
    # Basic analytics table
    analytics_sql = """
    CREATE TABLE IF NOT EXISTS analytics (
        id SERIAL PRIMARY KEY,
        metric_name VARCHAR(100) NOT NULL,
        metric_value DECIMAL(20,8),
        chain VARCHAR(50),
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        with engine.connect() as conn:
            # Create tables
            conn.execute(text(tokens_sql))
            conn.execute(text(wallets_sql))
            conn.execute(text(analytics_sql))
            conn.commit()
            print("✅ Tables created successfully!")
            
            # Insert sample data
            sample_sql = """
            INSERT INTO tokens (address, chain, name, symbol, decimals, risk_level, final_score) VALUES
            ('0x1234567890123456789012345678901234567890', 'base', 'Sample Token', 'SAMPLE', 18, 'low', 0.15),
            ('0x2345678901234567890123456789012345678901', 'base', 'Risk Token', 'RISK', 18, 'high', 0.85)
            ON CONFLICT (address) DO NOTHING;
            """
            conn.execute(text(sample_sql))
            conn.commit()
            print("✅ Sample data inserted!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_tables()
