import logging
from typing import Dict, Any, Optional, List
from neo4j import GraphDatabase, AsyncGraphDatabase

from config.settings import settings

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    
    def close(self):
        self.driver.close()
    
    def create_wallet_node(self, address: str, chain: str, properties: Dict[str, Any] = None):
        """Create or update a wallet node"""
        with self.driver.session() as session:
            query = """
            MERGE (w:Wallet {address: $address, chain: $chain})
            SET w += $properties
            RETURN w
            """
            session.run(query, address=address, chain=chain, properties=properties or {})
    
    def create_token_node(self, address: str, chain: str, properties: Dict[str, Any] = None):
        """Create or update a token node"""
        with self.driver.session() as session:
            query = """
            MERGE (t:Token {address: $address, chain: $chain})
            SET t += $properties
            RETURN t
            """
            session.run(query, address=address, chain=chain, properties=properties or {})
    
    def create_deployed_relationship(self, wallet_address: str, token_address: str, chain: str, properties: Dict[str, Any] = None):
        """Create DEPLOYED relationship between wallet and token"""
        with self.driver.session() as session:
            query = """
            MATCH (w:Wallet {address: $wallet_address, chain: $chain})
            MATCH (t:Token {address: $token_address, chain: $chain})
            MERGE (w)-[r:DEPLOYED]->(t)
            SET r += $properties
            RETURN r
            """
            session.run(
                query,
                wallet_address=wallet_address,
                token_address=token_address,
                chain=chain,
                properties=properties or {}
            )
    
    def create_funded_relationship(self, from_address: str, to_address: str, chain: str, properties: Dict[str, Any] = None):
        """Create FUNDED relationship between wallets"""
        with self.driver.session() as session:
            query = """
            MATCH (from:Wallet {address: $from_address, chain: $chain})
            MATCH (to:Wallet {address: $to_address, chain: $chain})
            MERGE (from)-[r:FUNDED]->(to)
            SET r += $properties
            RETURN r
            """
            session.run(
                query,
                from_address=from_address,
                to_address=to_address,
                chain=chain,
                properties=properties or {}
            )
    
    def get_wallet_cluster(self, wallet_address: str, chain: str, depth: int = 2) -> List[Dict]:
        """Get wallet cluster up to specified depth"""
        with self.driver.session() as session:
            query = f"""
            MATCH path = (w:Wallet {{address: $address, chain: $chain}})-[*1..{depth}]-(connected)
            RETURN path
            """
            result = session.run(query, address=wallet_address, chain=chain)
            # Process results
            return list(result)