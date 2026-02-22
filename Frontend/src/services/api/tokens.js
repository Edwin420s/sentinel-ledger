import apiClient from './client';

export const tokenApi = {
  getTokens: (params) => apiClient.get('/tokens', { params }),
  
  getToken: (address) => apiClient.get(`/tokens/${address}`),
  
  getRecentTokens: (limit = 10) => 
    apiClient.get('/tokens/recent', { params: { limit } }),
  
  getHighRiskTokens: (limit = 5) => 
    apiClient.get('/tokens/high-risk', { params: { limit } }),
  
  searchTokens: (query) => 
    apiClient.get('/tokens/search', { params: { q: query } }),
  
  getTokenStats: (address) => 
    apiClient.get(`/tokens/${address}/stats`),
  
  getTokenTransactions: (address, limit = 20) => 
    apiClient.get(`/tokens/${address}/transactions`, { params: { limit } }),
  
  getTokenHolders: (address, limit = 10) => 
    apiClient.get(`/tokens/${address}/holders`, { params: { limit } }),
  
  compareTokens: (addresses) => 
    apiClient.post('/tokens/compare', { addresses }),
};