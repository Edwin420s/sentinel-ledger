export const validators = {
  // Ethereum address validation
  isAddress: (address) => {
    return /^0x[a-fA-F0-9]{40}$/.test(address);
  },

  // Transaction hash validation
  isTxHash: (hash) => {
    return /^0x[a-fA-F0-9]{64}$/.test(hash);
  },

  // Token symbol validation
  isSymbol: (symbol) => {
    return /^[A-Z0-9]{2,10}$/.test(symbol);
  },

  // Risk score validation (0-100)
  isValidRiskScore: (score) => {
    const num = Number(score);
    return !isNaN(num) && num >= 0 && num <= 100;
  },

  // Chain validation
  isValidChain: (chain) => {
    return ['base', 'ethereum', 'both'].includes(chain);
  },

  // Timeframe validation
  isValidTimeframe: (timeframe) => {
    return ['24h', '7d', '30d', '90d', 'all'].includes(timeframe);
  },
};