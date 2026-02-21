from typing import Dict, Any, List, Optional
from web3 import Web3
import logging

logger = logging.getLogger(__name__)

class EventDecoder:
    def __init__(self, w3: Web3):
        self.w3 = w3
        
        # Common event signatures
        self.EVENT_SIGNATURES = {
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer",
            "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925": "Approval",
            "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1": "Sync",
            "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f": "Mint",
            "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496": "Burn",
            "0x783cca1c0412dd0d695e784568c96da2e9c22ff989357a2e8b1d9b2b4e6b7118": "PoolCreated",
        }
        
        # Event parameter types
        self.EVENT_PARAMS = {
            "Transfer": [
                {"name": "from", "type": "address", "indexed": True},
                {"name": "to", "type": "address", "indexed": True},
                {"name": "value", "type": "uint256", "indexed": False},
            ],
            "Approval": [
                {"name": "owner", "type": "address", "indexed": True},
                {"name": "spender", "type": "address", "indexed": True},
                {"name": "value", "type": "uint256", "indexed": False},
            ],
            "Sync": [
                {"name": "reserve0", "type": "uint112", "indexed": False},
                {"name": "reserve1", "type": "uint112", "indexed": False},
            ],
            "Mint": [
                {"name": "sender", "type": "address", "indexed": True},
                {"name": "amount0", "type": "uint256", "indexed": False},
                {"name": "amount1", "type": "uint256", "indexed": False},
            ],
            "Burn": [
                {"name": "sender", "type": "address", "indexed": True},
                {"name": "amount0", "type": "uint256", "indexed": False},
                {"name": "amount1", "type": "uint256", "indexed": False},
                {"name": "to", "type": "address", "indexed": True},
            ],
        }
    
    def decode_log(self, log: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Decode a log entry"""
        topics = log.get("topics", [])
        data = log.get("data", "0x")
        
        if not topics:
            return None
        
        event_signature = topics[0].hex() if hasattr(topics[0], 'hex') else topics[0]
        event_name = self.EVENT_SIGNATURES.get(event_signature)
        
        if not event_name:
            return None
        
        decoded = {
            "name": event_name,
            "address": log.get("address"),
            "block_number": log.get("blockNumber"),
            "transaction_hash": log.get("transactionHash"),
            "params": {}
        }
        
        # Decode parameters (simplified - in production use contract ABI)
        if event_name in self.EVENT_PARAMS:
            params = self.EVENT_PARAMS[event_name]
            topic_index = 1
            
            for param in params:
                if param["indexed"]:
                    if topic_index < len(topics):
                        value = topics[topic_index].hex()
                        decoded["params"][param["name"]] = value
                        topic_index += 1
            
            # Non-indexed params are in data
            if data and data != "0x":
                decoded["params"]["data"] = data
        
        return decoded