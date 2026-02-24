import apiClient from './client';
import { tokenApi } from './tokens';
import { walletApi } from './wallets';
import { analyticsApi } from './analytics';
import { wsService } from './websocket';

// Combined API object
export const api = {
  ...tokenApi,
  ...walletApi,
  ...analyticsApi,
  getDashboardStats: analyticsApi.getDashboardStats,
  getRecentTokens: tokenApi.getRecentTokens,
  getHighRiskTokens: tokenApi.getHighRiskTokens,
  getDeploymentTrends: analyticsApi.getDeploymentTrends,
};

export { apiClient, tokenApi, walletApi, analyticsApi, wsService };