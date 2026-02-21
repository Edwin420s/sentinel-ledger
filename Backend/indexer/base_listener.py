import asyncio
import logging
from typing import Optional
from datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware

from config.settings import settings
from config.chains import BASE
from db.session import SessionLocal
from db.models import ProcessedBlock
from indexer.block_processor import BlockProcessor

logger = logging.getLogger(__name__)

class BaseListener:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.BASE_RPC_URL))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.chain = BASE
        self.block_processor = BlockProcessor(self.w3, "base")
        self.running = False
        
    def get_last_processed_block(self) -> int:
        """Get last processed block from database"""
        db = SessionLocal()
        try:
            record = db.query(ProcessedBlock).filter(ProcessedBlock.chain == "base").first()
            if record:
                return record.block_number
            return self.chain.start_block
        finally:
            db.close()
    
    def update_last_processed_block(self, block_number: int, block_hash: str):
        """Update last processed block"""
        db = SessionLocal()
        try:
            record = db.query(ProcessedBlock).filter(ProcessedBlock.chain == "base").first()
            if record:
                record.block_number = block_number
                record.hash = block_hash
                record.processed_at = datetime.utcnow()
            else:
                record = ProcessedBlock(
                    chain="base",
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
    
    async def run(self):
        """Main listener loop"""
        self.running = True
        last_block = self.get_last_processed_block()
        
        logger.info(f"Starting Base listener from block {last_block}")
        
        while self.running:
            try:
                current_block = self.w3.eth.block_number
                
                if current_block <= last_block:
                    await asyncio.sleep(5)
                    continue
                
                # Process in batches
                start_block = last_block + 1
                end_block = min(current_block, start_block + settings.MAX_BLOCK_BATCH)
                
                logger.info(f"Processing blocks {start_block} to {end_block}")
                
                for block_num in range(start_block, end_block + 1):
                    try:
                        block = self.w3.eth.get_block(block_num, full_transactions=True)
                        await self.block_processor.process_block(block_num, block)
                        self.update_last_processed_block(block_num, block.hash.hex())
                    except Exception as e:
                        logger.error(f"Error processing block {block_num}: {e}")
                        # Continue to next block
                        continue
                
                last_block = end_block
                
                # Small delay between batches
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Listener error: {e}")
                await asyncio.sleep(10)
    
    def stop(self):
        """Stop the listener"""
        self.running = False
        logger.info("Base listener stopped")