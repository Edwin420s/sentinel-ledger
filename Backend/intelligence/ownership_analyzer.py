import logging
from typing import Dict, Any, Optional, List
from web3 import Web3

from db.session import SessionLocal
from db.models import Token, ContractAnalysis

logger = logging.getLogger(__name__)

class OwnershipAnalyzer:
    def __init__(self, w3: Web3, chain: str):
        self.w3 = w3
        self.chain = chain
        
        # Common ownership-related function selectors
        self.OWNERSHIP_SELECTORS = {
            "8da5cb5b": "owner()",  # owner()
            "f2fde38b": "transferOwnership",  # transferOwnership(address)
            "715018a6": "renounceOwnership",  # renounceOwnership()
            "13af4035": "setOwner",  # setOwner(address)
        }
        
        # Dangerous function selectors
        self.DANGEROUS_SELECTORS = {
            "42966c68": "burn",  # burn(uint256)
            "79cc6790": "burnFrom",  # burnFrom(address,uint256)
            "40c10f19": "mint",  # mint(address,uint256)
            "9dc29fac": "withdraw",  # withdraw(uint256)
            "24d7806c": "setMinter",  # setMinter(address)
            "9b2f3ef0": "setBlacklist",  # setBlacklist(address,bool)
            "f9f92be4": "addToBlacklist",  # addToBlacklist(address)
            "f0f9d4c6": "removeFromBlacklist",  # removeFromBlacklist(address)
            "8456cb59": "pause",  # pause()
            "3f4ba83a": "unpause",  # unpause()
            "8f283970": "setPauser",  # setPauser(address)
        }
    
    async def analyze(self, token_address: str) -> Dict[str, Any]:
        """Analyze token ownership and control structure"""
        token_address = Web3.to_checksum_address(token_address)
        
        try:
            # Get contract bytecode
            bytecode = self.w3.eth.get_code(token_address).hex()
            
            # Extract selectors
            selectors = self._extract_selectors(bytecode)
            
            # Check for ownership functions
            has_ownership = "8da5cb5b" in selectors
            has_transfer_ownership = "f2fde38b" in selectors
            has_renounce = "715018a6" in selectors
            
            # Check for dangerous functions
            dangerous_functions = []
            for selector, name in self.DANGEROUS_SELECTORS.items():
                if selector in selectors:
                    dangerous_functions.append(name)
            
            # Try to get current owner (if possible)
            current_owner = await self._get_owner(token_address)
            
            # Check if ownership is renounced
            ownership_renounced = False
            if current_owner and current_owner == "0x0000000000000000000000000000000000000000":
                ownership_renounced = True
            
            # Calculate ownership risk score
            score = 0
            flags = []
            
            if not ownership_renounced and has_ownership:
                score += 30
                flags.append("Ownership not renounced")
            
            if has_transfer_ownership:
                score += 20
                flags.append("Ownership can be transferred")
            
            if "mint" in dangerous_functions:
                score += 25
                flags.append("Has mint function")
            
            if "blacklist" in str(dangerous_functions):
                score += 20
                flags.append("Has blacklist function")
            
            if "pause" in str(dangerous_functions):
                score += 15
                flags.append("Can pause trading")
            
            if "withdraw" in dangerous_functions:
                score += 20
                flags.append("Owner can withdraw funds")
            
            # Store analysis
            await self._store_analysis(
                token_address=token_address,
                has_ownership=has_ownership,
                ownership_renounced=ownership_renounced,
                dangerous_functions=dangerous_functions,
                score=min(score, 100),
                flags=flags
            )
            
            return {
                "ownership_score": min(score, 100),
                "flags": flags,
                "has_ownership": has_ownership,
                "ownership_renounced": ownership_renounced,
                "dangerous_functions": dangerous_functions
            }
            
        except Exception as e:
            logger.error(f"Error analyzing ownership for {token_address}: {e}")
            return {"ownership_score": 50, "flags": ["Analysis failed"]}
    
    def _extract_selectors(self, bytecode: str) -> List[str]:
        """Extract function selectors from bytecode"""
        selectors = []
        if not bytecode or bytecode == "0x":
            return selectors
        
        bytecode = bytecode.lower().replace("0x", "")
        
        # Look for function selectors (PUSH4 + 4 bytes)
        for i in range(0, len(bytecode) - 10, 2):
            if bytecode[i:i+2] == "63":  # PUSH4 opcode
                selector = bytecode[i+2:i+10]
                if len(selector) == 8:
                    selectors.append(selector)
        
        return selectors
    
    async def _get_owner(self, token_address: str) -> Optional[str]:
        """Try to get the contract owner (if possible)"""
        # This would require contract ABI
        # For MVP, return None
        return None
    
    async def _store_analysis(self, token_address: str, has_ownership: bool,
                              ownership_renounced: bool, dangerous_functions: List[str],
                              score: int, flags: List[str]):
        """Store ownership analysis in database"""
        db = SessionLocal()
        try:
            analysis = db.query(ContractAnalysis).filter(
                ContractAnalysis.token_address == token_address.lower(),
                ContractAnalysis.chain == self.chain
            ).first()
            
            if not analysis:
                analysis = ContractAnalysis(
                    token_address=token_address.lower(),
                    chain=self.chain
                )
            
            analysis.has_ownership = has_ownership
            analysis.ownership_renounced = ownership_renounced
            analysis.suspicious_patterns = dangerous_functions
            
            db.add(analysis)
            
            # Update token ownership score
            token = db.query(Token).filter(
                Token.address == token_address.lower(),
                Token.chain == self.chain
            ).first()
            
            if token:
                token.ownership_score = score
                token.flags = token.flags + flags if token.flags else flags
            
            db.commit()
        except Exception as e:
            logger.error(f"Error storing ownership analysis: {e}")
            db.rollback()
        finally:
            db.close()