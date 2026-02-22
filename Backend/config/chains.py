from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ChainConfig:
    name: str
    chain_id: int
    start_block: int
    native_currency: str
    stable_coins: List[str]

    def __post_init__(self):
        self.stable_coins = [addr.lower() for addr in self.stable_coins]

    def get_rpc_url(self) -> str:
        """Get RPC URL from settings at runtime (avoids circular import)."""
        from config.settings import settings
        if self.name == "base":
            return settings.BASE_RPC_URL
        elif self.name == "ethereum":
            return settings.ETH_RPC_URL
        raise ValueError(f"Unknown chain: {self.name}")


# Base chain configuration
BASE = ChainConfig(
    name="base",
    chain_id=8453,
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
UNISWAP_UNIVERSAL_ROUTER = "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"

# WETH on Base
WETH_BASE = "0x4200000000000000000000000000000000000006"
USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"

# Aerodrome router on Base
AERODROME_ROUTER = "0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43"

# Known LP locker contracts on Base
KNOWN_LP_LOCKERS = [
    "0x0000000000000000000000000000000000000000",  # Burn address
    "0x000000000000000000000000000000000000dead",  # Dead address
    "0x663a5c229c09b049e36dce11a68fae7fb794be63",  # Unicrypt
    "0x71b91373acf3acbfe6a48f72cf7f001f8f7b98f6",  # Team Finance
]

# Event Signatures
TRANSFER_EVENT = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
SYNC_EVENT = "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"
MINT_EVENT = "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f"
BURN_EVENT = "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496"
POOL_CREATED_EVENT = "0x783cca1c0412dd0d695e784568c96da2e9c22ff989357a2e8b1d9b2b4e6b7118"
PAIR_CREATED_EVENT = "0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9"  # Aerodrome/UniswapV2