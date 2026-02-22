export { default as apiClient } from './client';
export { tokenApi } from './tokens';
export { walletApi } from './wallets';
export { analyticsApi } from './analytics';
export { wsService } from './websocket';

// Combined API object
export const api = {
  ...tokenApi,
  ...walletApi,
  ...analyticsApi,
};