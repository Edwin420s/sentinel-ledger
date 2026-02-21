import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Environment
    ENV: str = Field("development", env="ENV")
    
    # RPC Endpoints
    BASE_RPC_URL: str = Field(..., env="BASE_RPC_URL")
    ETH_RPC_URL: str = Field(..., env="ETH_RPC_URL")
    
    # Database
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    POSTGRES_DB: str = Field("sentinel", env="POSTGRES_DB")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    
    # Neo4j
    NEO4J_URI: str = Field("bolt://localhost:7687", env="NEO4J_URI")
    NEO4J_USER: str = Field("neo4j", env="NEO4J_USER")
    NEO4J_PASSWORD: str = Field(..., env="NEO4J_PASSWORD")
    
    # Redis
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = Field(None, env="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = Field("https://openrouter.ai/api/v1", env="OPENROUTER_BASE_URL")
    
    # Processing
    BATCH_INTERVAL_SECONDS: int = Field(120, env="BATCH_INTERVAL_SECONDS")
    MAX_BLOCK_BATCH: int = Field(100, env="MAX_BLOCK_BATCH")
    
    # Risk weights
    CONTRACT_RISK_WEIGHT: float = 0.35
    LIQUIDITY_RISK_WEIGHT: float = 0.30
    OWNERSHIP_RISK_WEIGHT: float = 0.20
    DEPLOYER_RISK_WEIGHT: float = 0.15
    
    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()