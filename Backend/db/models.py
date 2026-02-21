from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

Base = declarative_base()

class Token(Base):
    __tablename__ = "tokens"
    
    address = Column(String, primary_key=True, index=True)
    chain = Column(String, nullable=False, index=True)
    deployer = Column(String, nullable=False, index=True)
    deployer_original_chain = Column(String, nullable=True)
    deployed_block = Column(BigInteger, nullable=False)
    deployed_at = Column(DateTime(timezone=True), server_default=func.now())
    bytecode_hash = Column(String, nullable=True)
    name = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    decimals = Column(Integer, nullable=True)
    
    # Risk scores
    contract_score = Column(Float, default=0.0)
    liquidity_score = Column(Float, default=0.0)
    ownership_score = Column(Float, default=0.0)
    deployer_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    risk_level = Column(String, default="UNKNOWN")
    
    # Flags
    flags = Column(JSONB, default=[])
    
    # Analysis timestamps
    analyzed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    liquidity_pools = relationship("LiquidityPool", back_populates="token", cascade="all, delete-orphan")
    risk_history = relationship("RiskHistory", back_populates="token", cascade="all, delete-orphan")

class Wallet(Base):
    __tablename__ = "wallets"
    
    address = Column(String, primary_key=True, index=True)
    chain = Column(String, primary_key=True)
    first_seen_block = Column(BigInteger)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Statistics
    total_contracts = Column(Integer, default=0)
    erc20_count = Column(Integer, default=0)
    suspected_rugs = Column(Integer, default=0)
    avg_liquidity_duration_hours = Column(Float, default=0.0)
    wallet_age_days = Column(Integer, default=0)
    
    # Risk metrics
    deployer_risk_score = Column(Float, default=0.0)
    is_flagged = Column(Boolean, default=False)
    flags = Column(JSONB, default=[])
    
    # Cross-chain data
    base_activity = Column(JSONB, default={})
    ethereum_activity = Column(JSONB, default={})
    
    # Relationships
    deployed_tokens = relationship("Token", foreign_keys=[Token.deployer], primaryjoin="and_(Wallet.address==Token.deployer, Wallet.chain==Token.chain)")

class LiquidityPool(Base):
    __tablename__ = "liquidity_pools"
    
    id = Column(String, primary_key=True)  # chain:address
    token_address = Column(String, ForeignKey("tokens.address"), nullable=False, index=True)
    chain = Column(String, nullable=False)
    dex = Column(String, nullable=False)  # uniswap, aerodrome
    pool_address = Column(String, nullable=False)
    
    # Liquidity metrics
    initial_liquidity_usd = Column(Float, default=0.0)
    current_liquidity_usd = Column(Float, default=0.0)
    peak_liquidity_usd = Column(Float, default=0.0)
    liquidity_locked = Column(Boolean, default=False)
    lp_holder = Column(String, nullable=True)
    lp_lock_contract = Column(String, nullable=True)
    
    # Timing
    created_at_block = Column(BigInteger)
    created_at = Column(DateTime(timezone=True))
    first_liquidity_added_at = Column(DateTime(timezone=True), nullable=True)
    first_liquidity_removed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Flags
    removed_early = Column(Boolean, default=False)
    removal_percentage = Column(Float, default=0.0)
    
    # Relationship
    token = relationship("Token", back_populates="liquidity_pools")

class ContractAnalysis(Base):
    __tablename__ = "contract_analysis"
    
    token_address = Column(String, ForeignKey("tokens.address"), primary_key=True)
    chain = Column(String, primary_key=True)
    
    # Function presence
    has_mint = Column(Boolean, default=False)
    mint_restricted = Column(Boolean, default=True)  # True if owner-only
    has_blacklist = Column(Boolean, default=False)
    has_pause = Column(Boolean, default=False)
    has_ownership = Column(Boolean, default=False)
    ownership_renounced = Column(Boolean, default=False)
    is_proxy = Column(Boolean, default=False)
    upgradeable = Column(Boolean, default=False)
    can_change_fees = Column(Boolean, default=False)
    can_withdraw = Column(Boolean, default=False)
    
    # Bytecode analysis
    suspicious_patterns = Column(JSONB, default=[])
    function_selectors = Column(JSONB, default=[])
    
    # Analysis metadata
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    token = relationship("Token")

class RiskHistory(Base):
    __tablename__ = "risk_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_address = Column(String, ForeignKey("tokens.address"), nullable=False)
    chain = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    level = Column(String, nullable=False)
    flags = Column(JSONB, default=[])
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    token = relationship("Token", back_populates="risk_history")

class ProcessedBlock(Base):
    __tablename__ = "processed_blocks"
    
    chain = Column(String, primary_key=True)
    block_number = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    hash = Column(String, nullable=True)