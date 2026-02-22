import logging
from typing import Dict, Any, Optional, List
from web3 import Web3

from config.chains import AERODROME_FACTORY, WETH_BASE, USDC_BASE

logger = logging.getLogger(__name__)

# Aerodrome factory ABI — supports both stable and volatile pairs
AERODROME_FACTORY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "tokenA", "type": "address"},
            {"internalType": "address", "name": "tokenB", "type": "address"},
            {"internalType": "bool", "name": "stable", "type": "bool"},
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]

# Minimal Aerodrome pool ABI
AERODROME_POOL_ABI = [
    {
        "inputs": [],
        "name": "reserve0",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "reserve1",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
    {
        "inputs": [],
        "name": "stable",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

PAIRED_TOKENS_BASE = [WETH_BASE, USDC_BASE]
POOL_TYPES = [False, True]  # volatile=False, stable=True


class AerodromeTracker:
    """Tracks Aerodrome V2/CL liquidity pools on Base for a given ERC-20 token."""

    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.factory = self.w3.eth.contract(
            address=Web3.to_checksum_address(AERODROME_FACTORY),
            abi=AERODROME_FACTORY_ABI,
        )

    def detect_pool(self, token_address: str) -> Optional[Dict[str, Any]]:
        """
        Query the Aerodrome factory for both volatile and stable pools paired
        against WETH and USDC. Returns first found pool or None.
        """
        token_cs = Web3.to_checksum_address(token_address)

        for paired in PAIRED_TOKENS_BASE:
            paired_cs = Web3.to_checksum_address(paired)
            for stable in POOL_TYPES:
                try:
                    pool_address = self.factory.functions.getPool(
                        token_cs, paired_cs, stable
                    ).call()

                    if pool_address == "0x0000000000000000000000000000000000000000":
                        continue

                    logger.info(
                        f"Aerodrome pool found for {token_address}: {pool_address} "
                        f"(stable={stable}, pair={paired})"
                    )

                    pool_info = self.get_pool_info(pool_address)
                    if pool_info:
                        pool_info["paired_with"] = paired.lower()
                        pool_info["stable"] = stable
                        return pool_info

                except Exception as e:
                    logger.debug(
                        f"No Aerodrome pool for {token_address} / {paired} / stable={stable}: {e}"
                    )

        return None

    def get_pool_info(self, pool_address: str) -> Optional[Dict[str, Any]]:
        """Fetch reserves, token addresses and supply from the pool contract."""
        try:
            pool_cs = Web3.to_checksum_address(pool_address)
            pool = self.w3.eth.contract(address=pool_cs, abi=AERODROME_POOL_ABI)

            token0 = pool.functions.token0().call()
            token1 = pool.functions.token1().call()
            reserve0 = pool.functions.reserve0().call()
            reserve1 = pool.functions.reserve1().call()
            total_supply = pool.functions.totalSupply().call()
            is_stable = pool.functions.stable().call()

            return {
                "address": pool_address.lower(),
                "dex": "aerodrome",
                "token0": token0.lower(),
                "token1": token1.lower(),
                "reserve0": reserve0,
                "reserve1": reserve1,
                "total_supply": total_supply,
                "stable": is_stable,
                "created_at_block": None,
            }
        except Exception as e:
            logger.error(f"Error fetching Aerodrome pool info for {pool_address}: {e}")
            return None

    def get_reserves(self, pool_address: str) -> Dict[str, int]:
        """Fetch current reserves from a pool."""
        try:
            pool_cs = Web3.to_checksum_address(pool_address)
            pool = self.w3.eth.contract(address=pool_cs, abi=AERODROME_POOL_ABI)
            return {
                "reserve0": pool.functions.reserve0().call(),
                "reserve1": pool.functions.reserve1().call(),
            }
        except Exception as e:
            logger.error(f"Error fetching Aerodrome reserves for {pool_address}: {e}")
            return {"reserve0": 0, "reserve1": 0}