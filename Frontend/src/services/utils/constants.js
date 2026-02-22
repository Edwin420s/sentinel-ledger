export const CHAINS = {
  BASE: 'base',
  ETHEREUM: 'ethereum',
};

export const CHAIN_NAMES = {
  [CHAINS.BASE]: 'Base',
  [CHAINS.ETHEREUM]: 'Ethereum',
};

export const CHAIN_COLORS = {
  [CHAINS.BASE]: '#14b8a6',
  [CHAINS.ETHEREUM]: '#627eea',
};

export const RISK_LEVELS = {
  LOW: 'LOW',
  MODERATE: 'MODERATE',
  HIGH: 'HIGH',
  CRITICAL: 'CRITICAL',
};

export const RISK_COLORS = {
  [RISK_LEVELS.LOW]: '#22c55e',
  [RISK_LEVELS.MODERATE]: '#f59e0b',
  [RISK_LEVELS.HIGH]: '#f97316',
  [RISK_LEVELS.CRITICAL]: '#ef4444',
};

export const RISK_THRESHOLDS = {
  [RISK_LEVELS.LOW]: 30,
  [RISK_LEVELS.MODERATE]: 60,
  [RISK_LEVELS.HIGH]: 80,
  [RISK_LEVELS.CRITICAL]: 100,
};

export const DEX_TYPES = {
  UNISWAP: 'uniswap',
  AERODROME: 'aerodrome',
  OTHER: 'other',
};

export const DEX_NAMES = {
  [DEX_TYPES.UNISWAP]: 'Uniswap',
  [DEX_TYPES.AERODROME]: 'Aerodrome',
  [DEX_TYPES.OTHER]: 'Other DEX',
};

export const EVENT_TYPES = {
  NEW_TOKEN: 'new_token',
  HIGH_RISK: 'high_risk',
  RUG_DETECTED: 'rug_detected',
  LIQUIDITY_CHANGE: 'liquidity_change',
  OWNERSHIP_CHANGE: 'ownership_change',
};

export const FLAG_SEVERITIES = {
  INFO: 'info',
  WARNING: 'warning',
  CRITICAL: 'critical',
};

export const TIME_FRAMES = {
  '24h': 24 * 60 * 60 * 1000,
  '7d': 7 * 24 * 60 * 60 * 1000,
  '30d': 30 * 24 * 60 * 60 * 1000,
  '90d': 90 * 24 * 60 * 60 * 1000,
};

export const API_ENDPOINTS = {
  TOKENS: '/tokens',
  WALLETS: '/wallets',
  ANALYTICS: '/analytics',
  RISK_FEED: '/risk-feed',
  HEALTH: '/health',
};

export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;
export const REFRESH_INTERVAL = 30000; // 30 seconds
export const WEBSOCKET_RECONNECT_ATTEMPTS = 5;
export const WEBSOCKET_RECONNECT_DELAY = 1000;