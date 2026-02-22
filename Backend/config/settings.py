from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Environment
    ENV: str = Field("development")

    # RPC Endpoints
    BASE_RPC_URL: str = Field(..., alias="BASE_RPC_URL")
    ETH_RPC_URL: str = Field(..., alias="ETH_RPC_URL")

    # Database
    POSTGRES_HOST: str = Field("localhost")
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_DB: str = Field("sentinel")
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)

    # Neo4j
    NEO4J_URI: str = Field("bolt://localhost:7687")
    NEO4J_USER: str = Field("neo4j")
    NEO4J_PASSWORD: str = Field(...)

    # Redis
    REDIS_URL: str = Field("redis://localhost:6379")

    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = Field(None)
    OPENROUTER_BASE_URL: str = Field("https://openrouter.ai/api/v1")

    # Processing
    BATCH_INTERVAL_SECONDS: int = Field(120)
    MAX_BLOCK_BATCH: int = Field(100)

    # Risk weights
    CONTRACT_RISK_WEIGHT: float = 0.35
    LIQUIDITY_RISK_WEIGHT: float = 0.30
    OWNERSHIP_RISK_WEIGHT: float = 0.20
    DEPLOYER_RISK_WEIGHT: float = 0.15

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "populate_by_name": True,
    }


settings = Settings()