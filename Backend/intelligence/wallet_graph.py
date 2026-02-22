import logging
from typing import Dict, Any, Optional, List
from web3 import Web3

from db.session import SessionLocal
from db.models import Wallet, Token
from graph.neo4j_client import Neo4jClient

logger = logging.getLogger(__name__)


class WalletGraph:
    """
    Builds and queries the Neo4j graph of wallet relationships.
    Responsible for:
    - Creating Wallet and Token nodes in the graph
    - Creating DEPLOYED, FUNDED, ADDED_LIQUIDITY edges
    - Querying cluster risk based on graph topology
    """

    def __init__(self, neo4j_client: Optional[Neo4jClient] = None):
        self.neo4j: Optional[Neo4jClient] = neo4j_client

    def _graph_available(self) -> bool:
        return self.neo4j is not None

    # ------------------------------------------------------------------
    # Node creation
    # ------------------------------------------------------------------
    def record_token_deployment(
        self,
        deployer: str,
        token_address: str,
        chain: str,
        block_number: int,
    ) -> None:
        """
        Create/update Wallet + Token nodes and the DEPLOYED edge.
        Safe to call even if Neo4j is unavailable.
        """
        if not self._graph_available():
            return
        try:
            self.neo4j.create_wallet_node(
                address=deployer.lower(),
                chain=chain,
                properties={"chain": chain},
            )
            self.neo4j.create_token_node(
                address=token_address.lower(),
                chain=chain,
                properties={"chain": chain, "deployed_block": block_number},
            )
            self.neo4j.create_deployed_relationship(
                wallet_address=deployer.lower(),
                token_address=token_address.lower(),
                chain=chain,
                properties={"block_number": block_number},
            )
            logger.debug(f"Graph: recorded deployment {deployer} → {token_address}")
        except Exception as e:
            logger.error(f"Graph: failed to record deployment for {token_address}: {e}")

    def record_funding(
        self,
        from_address: str,
        to_address: str,
        chain: str,
        tx_hash: str,
        amount_eth: float = 0.0,
    ) -> None:
        """Create a FUNDED edge between two wallet nodes."""
        if not self._graph_available():
            return
        try:
            for addr in (from_address, to_address):
                self.neo4j.create_wallet_node(address=addr.lower(), chain=chain)
            self.neo4j.create_funded_relationship(
                from_address=from_address.lower(),
                to_address=to_address.lower(),
                chain=chain,
                properties={"transaction_hash": tx_hash, "amount_eth": amount_eth},
            )
        except Exception as e:
            logger.error(f"Graph: failed to record funding {from_address}→{to_address}: {e}")

    # ------------------------------------------------------------------
    # Risk queries
    # ------------------------------------------------------------------
    def get_cluster_risk(self, wallet_address: str, chain: str, depth: int = 2) -> Dict[str, Any]:
        """
        Query the neighbourhood of a wallet in the graph and assess cluster risk.
        Returns a dict with risk_score and flags derived from graph topology.
        """
        if not self._graph_available():
            return {"cluster_risk_score": 0, "flags": [], "cluster_size": 0}

        try:
            cluster = self.neo4j.get_wallet_cluster(wallet_address.lower(), chain, depth)
            cluster_size = len(cluster)
        except Exception as e:
            logger.error(f"Graph: cluster query failed for {wallet_address}: {e}")
            return {"cluster_risk_score": 0, "flags": [], "cluster_size": 0}

        score = 0
        flags: List[str] = []

        # Large clusters with shared funding are high risk
        if cluster_size > 20:
            score += 30
            flags.append(f"Large connected cluster ({cluster_size} nodes)")
        elif cluster_size > 10:
            score += 15
            flags.append(f"Moderate cluster size ({cluster_size} nodes)")

        return {
            "cluster_risk_score": min(score, 100),
            "flags": flags,
            "cluster_size": cluster_size,
        }

    # ------------------------------------------------------------------
    # Sync wallet data from Postgres → Neo4j (batch initialisation)
    # ------------------------------------------------------------------
    def sync_from_postgres(self) -> None:
        """
        Read all wallets and tokens from the Postgres DB and create/update
        the corresponding Neo4j nodes. Useful for initial graph population.
        """
        if not self._graph_available():
            logger.warning("WalletGraph: Neo4j not available, skipping sync")
            return

        db = SessionLocal()
        try:
            # Sync tokens
            tokens = db.query(Token).all()
            for tok in tokens:
                self.neo4j.create_wallet_node(
                    address=tok.deployer, chain=tok.chain,
                    properties={"chain": tok.chain},
                )
                self.neo4j.create_token_node(
                    address=tok.address, chain=tok.chain,
                    properties={
                        "chain": tok.chain,
                        "risk_level": tok.risk_level or "UNKNOWN",
                        "final_score": tok.final_score or 0.0,
                    },
                )
                self.neo4j.create_deployed_relationship(
                    wallet_address=tok.deployer,
                    token_address=tok.address,
                    chain=tok.chain,
                    properties={"block_number": tok.deployed_block},
                )

            logger.info(f"WalletGraph: synced {len(tokens)} tokens to Neo4j")
        except Exception as e:
            logger.error(f"WalletGraph: sync_from_postgres failed: {e}")
        finally:
            db.close()
