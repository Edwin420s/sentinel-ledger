import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const api = {
  // Tokens
  getTokens: (params) => apiClient.get('/tokens', { params }),
  getToken: (address) => apiClient.get(`/tokens/${address}`),
  getRecentTokens: (limit = 10) => apiClient.get('/tokens/recent', { params: { limit } }),
  getHighRiskTokens: (limit = 5) => apiClient.get('/tokens/high-risk', { params: { limit } }),
  
  // Wallets
  getWallet: (address) => apiClient.get(`/wallets/${address}`),
  getWalletTokens: (address) => apiClient.get(`/wallets/${address}/tokens`),
  
  // Analytics
  getDashboardStats: () => apiClient.get('/analytics/dashboard'),
  getRiskDistribution: () => apiClient.get('/analytics/risk-distribution'),
  getDeploymentTrends: () => apiClient.get('/analytics/deployment-trends'),
};

export default api;