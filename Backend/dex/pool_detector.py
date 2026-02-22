import logging
from typing import Dict, Any, Optional
from web3 import Web3

from dex.uniswap import UniswapTracker
from dex.aerodrome import AerodromeTracker

logger = logging.getLogger(__name__)


class PoolDetector:
    """
    Unified pool detector that checks both Uniswap V3 and Aerodrome
    and returns the first discovered pool along with its source DEX.
    """

    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.uniswap = UniswapTracker(w3, chain)
        self.aerodrome = AerodromeTracker(w3, chain)

    def detect(self, token_address: str) -> Optional[Dict[str, Any]]:
        """
        Return the first pool found across all supported DEXes,
        or None if the token has no pool yet.
        """
        token_address = token_address.lower()

        uni_pool = self.uniswap.detect_pool(token_address)
        if uni_pool:
            uni_pool["source"] = "uniswap_v3"
            return uni_pool

        aero_pool = self.aerodrome.detect_pool(token_address)
        if aero_pool:
            aero_pool["source"] = "aerodrome"
            return aero_pool

        logger.debug(f"No DEX pool found for {token_address} on {self.chain}")
        return None

    def detect_all(self, token_address: str) -> list[Dict[str, Any]]:
        """
        Return every pool found across all supported DEXes for a token.
        """
        pools = []
        uni_pool = self.uniswap.detect_pool(token_address.lower())
        if uni_pool:
            uni_pool["source"] = "uniswap_v3"
            pools.append(uni_pool)

        aero_pool = self.aerodrome.detect_pool(token_address.lower())
        if aero_pool:
            aero_pool["source"] = "aerodrome"
            pools.append(aero_pool)

        return pools
