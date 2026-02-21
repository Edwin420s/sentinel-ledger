import logging
import json
from typing import Dict, Any, List, Optional
import httpx

from config.settings import settings

logger = logging.getLogger(__name__)

class ExplanationEngine:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = "openai/gpt-3.5-turbo"  # Default model
        
    async def generate_explanation(self, token_data: Dict[str, Any]) -> Optional[str]:
        """Generate AI explanation for token risk"""
        if not self.api_key:
            logger.warning("OpenRouter API key not configured")
            return None
        
        try:
            # Prepare prompt
            prompt = self._build_prompt(token_data)
            
            # Call OpenRouter API
            explanation = await self._call_llm(prompt)
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return None
    
    def _build_prompt(self, data: Dict[str, Any]) -> str:
        """Build prompt for LLM"""
        prompt = f"""You are a blockchain security analyst. Generate a concise, professional risk explanation for this token:

Token Address: {data.get('address')}
Chain: {data.get('chain')}
Risk Score: {data.get('final_score')}/100
Risk Level: {data.get('risk_level')}

Risk Breakdown:
- Contract Risk: {data.get('contract_score')}/100
- Liquidity Risk: {data.get('liquidity_score')}/100
- Ownership Risk: {data.get('ownership_score')}/100
- Deployer Risk: {data.get('deployer_score')}/100

Flags: {', '.join(data.get('flags', []))}

Deployer Information:
- Total Tokens: {data.get('deployer_total_tokens', 0)}
- Prior Suspected Rugs: {data.get('deployer_rugs', 0)}
- Wallet Age: {data.get('wallet_age_days', 0)} days

Generate a 2-3 sentence professional risk summary focusing on the most critical factors. Be factual, neutral, and avoid speculation."""
        
        return prompt
    
    async def _call_llm(self, prompt: str) -> str:
        """Call OpenRouter API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a blockchain security analyst providing factual risk assessments."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 150
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return "Unable to generate explanation at this time."