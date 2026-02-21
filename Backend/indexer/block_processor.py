import logging
from typing import Dict, Any
from web3 import Web3

from indexer.contract_detector import ContractDetector

logger = logging.getLogger(__name__)

class BlockProcessor:
    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.contract_detector = ContractDetector(w3, chain)
    
    async def process_block(self, block_number: int, block: Dict[str, Any]):
        """Process a single block"""
        logger.debug(f"Processing block {block_number} on {self.chain}")
        
        transactions = block.get("transactions", [])
        
        for tx in transactions:
            # Check if this is a contract creation transaction
            if tx.get("to") is None:
                await self._process_contract_creation(tx, block_number)
    
    async def _process_contract_creation(self, tx: Dict[str, Any], block_number: int):
        """Process a contract creation transaction"""
        tx_hash = tx.get("hash")
        
        try:
            # Get transaction receipt to get contract address
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            contract_address = receipt.get("contractAddress")
            
            if not contract_address:
                return
            
            deployer = tx.get("from")
            
            logger.info(f"New contract detected: {contract_address} on {self.chain} from {deployer}")
            
            # Process the contract
            await self.contract_detector.process_contract(
                contract_address=contract_address,
                deployer=deployer,
                block_number=block_number,
                tx_hash=tx_hash.hex() if hasattr(tx_hash, 'hex') else tx_hash
            )
            
        except Exception as e:
            logger.error(f"Error processing contract creation for tx {tx_hash}: {e}")