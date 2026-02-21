from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ChainConfig:
    name: str
    chain_id: int
    rpc_url: str
    start_block: int
    native_currency: str
    stable_coins: List[str]
    
    def __post_init__(self):
        self.stable_coins = [addr.lower() for addr in self.stable_coins]

# Base chain configuration
BASE = ChainConfig(
    name="base",
    chain_id=8453,
    rpc_url=settings.BASE_RPC_URL,  # Will be set from env
    start_block=0,
    native_currency="ETH",
    stable_coins=[
        "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",  # USDC
        "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca",  # USDbC
    ]
)

# Ethereum chain configuration
ETHEREUM = ChainConfig(
    name="ethereum",
    chain_id=1,
    rpc_url=settings.ETH_RPC_URL,  # Will be set from env
    start_block=0,
    native_currency="ETH",
    stable_coins=[
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
    ]
)

# DEX Factory Addresses
UNISWAP_V3_FACTORY = "0x33128a8fc17869897dce68ed026d694621f6fdfd"  # Base
AERODROME_FACTORY = "0x420dd381b31aef6683db6b902084cb0ffece40da"  # Base

# Event Signatures
TRANSFER_EVENT = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
SYNC_EVENT = "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"
MINT_EVENT = "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f"
BURN_EVENT = "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496"
POOL_CREATED_EVENT = "0x783cca1c0412dd0d695e784568c96da2e9c22ff989357a2e8b1d9b2b4e6b7118"