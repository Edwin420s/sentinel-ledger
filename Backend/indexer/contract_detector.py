import logging
from typing import Optional
from web3 import Web3

from db.session import SessionLocal
from db.models import Token
from indexer.erc20_classifier import ERC20Classifier
from tasks.job_runner import trigger_token_analysis

logger = logging.getLogger(__name__)

class ContractDetector:
    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        self.erc20_classifier = ERC20Classifier(w3)
    
    async def process_contract(self, contract_address: str, deployer: str, block_number: int, tx_hash: str):
        """Process a newly deployed contract"""
        
        # Check if already processed
        db = SessionLocal()
        try:
            existing = db.query(Token).filter(
                Token.address == contract_address.lower(),
                Token.chain == self.chain
            ).first()
            
            if existing:
                logger.debug(f"Contract {contract_address} already processed")
                return
            
            # Get bytecode
            bytecode = self.w3.eth.get_code(Web3.to_checksum_address(contract_address))
            
            if not bytecode or bytecode.hex() == "0x":
                logger.debug(f"Contract {contract_address} has no bytecode")
                return
            
            # Classify as ERC20
            is_erc20 = self.erc20_classifier.is_erc20(bytecode.hex())
            
            if not is_erc20:
                logger.debug(f"Contract {contract_address} is not ERC20")
                return
            
            # Store token
            token = Token(
                address=contract_address.lower(),
                chain=self.chain,
                deployer=deployer.lower(),
                deployed_block=block_number,
                bytecode_hash=Web3.keccak(bytecode).hex()
            )
            
            db.add(token)
            db.commit()
            
            logger.info(f"New ERC20 token detected: {contract_address} on {self.chain}")
            
            # Trigger async analysis
            trigger_token_analysis.delay(
                token_address=contract_address.lower(),
                chain=self.chain
            )
            
        except Exception as e:
            logger.error(f"Error processing contract {contract_address}: {e}")
            db.rollback()
        finally:
            db.close()