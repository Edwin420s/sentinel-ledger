from web3 import Web3
from typing import Optional, Dict, Any

def to_checksum_address(address: str) -> str:
    """Convert address to checksum format"""
    return Web3.to_checksum_address(address)

def is_valid_address(address: str) -> bool:
    """Check if address is valid"""
    return Web3.is_address(address)

def wei_to_ether(wei: int) -> float:
    """Convert wei to ether"""
    return Web3.from_wei(wei, 'ether')

def ether_to_wei(ether: float) -> int:
    """Convert ether to wei"""
    return Web3.to_wei(ether, 'ether')

def get_function_selector(function_signature: str) -> str:
    """Get 4-byte function selector from signature"""
    return Web3.keccak(text=function_signature).hex()[:10]

def decode_transaction_input(input_data: str) -> Dict[str, Any]:
    """Decode transaction input data"""
    # Basic implementation
    if not input_data or input_data == "0x":
        return {}
    
    # Remove 0x prefix
    data = input_data[2:] if input_data.startswith("0x") else input_data
    
    # First 8 characters are function selector
    selector = data[:8]
    
    return {
        "selector": f"0x{selector}",
        "data": f"0x{data[8:]}"
    }