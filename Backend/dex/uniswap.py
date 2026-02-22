import logging
from typing import Dict, Any, Optional, List
from web3 import Web3

from config.chains import UNISWAP_V3_FACTORY, WETH_BASE, USDC_BASE

logger = logging.getLogger(__name__)

# Minimal ABI for Uniswap V3 Factory's getPool() function
UNISWAP_V3_FACTORY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "tokenA", "type": "address"},
            {"internalType": "address", "name": "tokenB", "type": "address"},
            {"internalType": "uint24", "name": "fee", "type": "uint24"},
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]

# Minimal ABI to read Uniswap V3 pool slot0 + liquidity
UNISWAP_V3_POOL_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24", "name": "tick", "type": "int24"},
            {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
            {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool", "name": "unlocked", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "liquidity",
        "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# Standard Uniswap V3 fee tiers
FEE_TIERS = [100, 500, 3000, 10000]  # 0.01%, 0.05%, 0.3%, 1%

# Paired tokens to search for pools against
PAIRED_TOKENS_BASE = [
    WETH_BASE,
    USDC_BASE,
]


class UniswapTracker:
    """Tracks Uniswap V3 liquidity pools on Base for a given ERC-20 token."""

    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.factory = self.w3.eth.contract(
            address=Web3.to_checksum_address(UNISWAP_V3_FACTORY),
            abi=UNISWAP_V3_FACTORY_ABI,
        )

    def detect_pool(self, token_address: str) -> Optional[Dict[str, Any]]:
        """
        Query the Uniswap V3 factory for all fee-tier pools paired against
        WETH and USDC. Returns the first found pool, or None.
        """
        token_cs = Web3.to_checksum_address(token_address)

        for paired in PAIRED_TOKENS_BASE:
            paired_cs = Web3.to_checksum_address(paired)
            for fee in FEE_TIERS:
                try:
                    pool_address = self.factory.functions.getPool(
                        token_cs, paired_cs, fee
                    ).call()

                    if pool_address == "0x0000000000000000000000000000000000000000":
                        continue

                    logger.info(
                        f"Uniswap V3 pool found for {token_address}: {pool_address} "
                        f"(fee={fee}, pair={paired})"
                    )

                    pool_info = self.get_pool_info(pool_address)
                    if pool_info:
                        pool_info["paired_with"] = paired.lower()
                        pool_info["fee_tier"] = fee
                        return pool_info

                except Exception as e:
                    logger.debug(
                        f"No Uniswap V3 pool for {token_address} / {paired} / fee={fee}: {e}"
                    )

        return None

    def get_pool_info(self, pool_address: str) -> Optional[Dict[str, Any]]:
        """Fetch token0, token1 and current liquidity from the pool contract."""
        try:
            pool_cs = Web3.to_checksum_address(pool_address)
            pool = self.w3.eth.contract(address=pool_cs, abi=UNISWAP_V3_POOL_ABI)

            token0 = pool.functions.token0().call()
            token1 = pool.functions.token1().call()
            liquidity = pool.functions.liquidity().call()

            return {
                "address": pool_address.lower(),
                "dex": "uniswap_v3",
                "token0": token0.lower(),
                "token1": token1.lower(),
                "liquidity": liquidity,
                "created_at_block": None,  # Not available from pool directly
            }
        except Exception as e:
            logger.error(f"Error fetching Uniswap V3 pool info for {pool_address}: {e}")
            return None

    def get_liquidity_data(self, pool_address: str) -> Dict[str, Any]:
        """Get current liquidity for a pool in raw units."""
        try:
            pool_cs = Web3.to_checksum_address(pool_address)
            pool = self.w3.eth.contract(address=pool_cs, abi=UNISWAP_V3_POOL_ABI)
            liquidity = pool.functions.liquidity().call()
            return {"raw_liquidity": liquidity}
        except Exception as e:
            logger.error(f"Error fetching liquidity for {pool_address}: {e}")
            return {"raw_liquidity": 0}