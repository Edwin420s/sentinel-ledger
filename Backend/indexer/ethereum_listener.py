import asyncio
import logging
from web3 import Web3

from config.settings import settings
from config.chains import ETHEREUM
from indexer.base_listener import BaseListener

logger = logging.getLogger(__name__)

class EthereumListener(BaseListener):
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ETH_RPC_URL))
        self.chain = ETHEREUM
        self.block_processor = BlockProcessor(self.w3, "ethereum")
        self.running = False
    
    def get_last_processed_block(self) -> int:
        """Get last processed block from database"""
        db = SessionLocal()
        try:
            record = db.query(ProcessedBlock).filter(ProcessedBlock.chain == "ethereum").first()
            if record:
                return record.block_number
            return self.chain.start_block
        finally:
            db.close()
    
    def update_last_processed_block(self, block_number: int, block_hash: str):
        """Update last processed block"""
        db = SessionLocal()
        try:
            record = db.query(ProcessedBlock).filter(ProcessedBlock.chain == "ethereum").first()
            if record:
                record.block_number = block_number
                record.hash = block_hash
                record.processed_at = datetime.utcnow()
            else:
                record = ProcessedBlock(
                    chain="ethereum",
                    block_number=block_number,
                    hash=block_hash
                )
                db.add(record)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to update last processed block: {e}")
            db.rollback()
        finally:
            db.close()