# Neo4j Graph Schema Definition

NODE_LABELS = {
    "Wallet": {
        "properties": [
            "address",
            "chain",
            "first_seen",
            "total_contracts",
            "suspected_rugs",
            "risk_score"
        ]
    },
    "Token": {
        "properties": [
            "address",
            "chain",
            "deployer",
            "deployed_block",
            "final_score",
            "risk_level"
        ]
    },
    "Pool": {
        "properties": [
            "address",
            "dex",
            "token0",
            "token1",
            "created_at"
        ]
    }
}

RELATIONSHIP_TYPES = {
    "DEPLOYED": {
        "from": "Wallet",
        "to": "Token",
        "properties": ["block_number", "timestamp"]
    },
    "FUNDED": {
        "from": "Wallet",
        "to": "Wallet",
        "properties": ["amount", "transaction_hash"]
    },
    "ADDED_LIQUIDITY": {
        "from": "Wallet",
        "to": "Pool",
        "properties": ["amount0", "amount1", "block_number"]
    },
    "REMOVED_LIQUIDITY": {
        "from": "Wallet",
        "to": "Pool",
        "properties": ["amount0", "amount1", "block_number"]
    },
    "BRIDGED_TO": {
        "from": "Wallet",
        "to": "Wallet",
        "properties": ["chain_from", "chain_to", "amount"]
    }
}