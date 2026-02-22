import apiClient from './client';

export const walletApi = {
  getWallet: (address) => apiClient.get(`/wallets/${address}`),
  
  getWalletTokens: (address) => 
    apiClient.get(`/wallets/${address}/tokens`),
  
  getWalletTransactions: (address, limit = 10) => 
    apiClient.get(`/wallets/${address}/transactions`, { params: { limit } }),
  
  getWalletStats: (address) => 
    apiClient.get(`/wallets/${address}/stats`),
  
  getWalletGraph: (address, depth = 2) => 
    apiClient.get(`/wallets/${address}/graph`, { params: { depth } }),
  
  searchWallets: (query) => 
    apiClient.get('/wallets/search', { params: { q: query } }),
  
  getTopDeployers: (limit = 10) => 
    apiClient.get('/wallets/top-deployers', { params: { limit } }),
};