import logging
from typing import Set
from web3 import Web3

logger = logging.getLogger(__name__)

class ERC20Classifier:
    # ERC20 required function selectors
    ERC20_SELECTORS = {
        "18160ddd",  # totalSupply()
        "70a08231",  # balanceOf(address)
        "a9059cbb",  # transfer(address,uint256)
        "95ea7b3",   # approve(address,uint256)
        "23b872dd",  # transferFrom(address,address,uint256)
    }
    
    # Common optional selectors
    OPTIONAL_SELECTORS = {
        "06fdde03",  # name()
        "95d89b41",  # symbol()
        "313ce567",  # decimals()
    }
    
    def __init__(self, w3: Web3):
        self.w3 = w3
    
    def is_erc20(self, bytecode: str) -> bool:
        """
        Determine if contract is ERC20 by checking for required function selectors
        """
        if not bytecode or bytecode == "0x":
            return False
        
        # Convert to lowercase for matching
        bytecode = bytecode.lower()
        
        # Count required selectors
        required_matches = 0
        for selector in self.ERC20_SELECTORS:
            if selector in bytecode:
                required_matches += 1
        
        # At least 3 of 5 required selectors must be present
        return required_matches >= 3
    
    def extract_selectors(self, bytecode: str) -> Set[str]:
        """
        Extract all function selectors from bytecode
        """
        selectors = set()
        if not bytecode or bytecode == "0x":
            return selectors
        
        bytecode = bytecode.lower().replace("0x", "")
        
        # Look for function selectors (4-byte signatures)
        # Common pattern: 63xxxxxx (PUSH4) followed by selector
        for i in range(0, len(bytecode) - 10, 2):
            if bytecode[i:i+2] == "63":  # PUSH4 opcode
                selector = bytecode[i+2:i+10]
                if len(selector) == 8:
                    selectors.add(selector)
        
        return selectors