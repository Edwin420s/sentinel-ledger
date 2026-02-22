import apiClient from './client';

export const analyticsApi = {
  getDashboardStats: () => apiClient.get('/analytics/dashboard'),
  
  getRiskDistribution: () => apiClient.get('/analytics/risk-distribution'),
  
  getRiskTrends: (timeframe = '7d') => 
    apiClient.get('/analytics/risk-trends', { params: { timeframe } }),
  
  getDeploymentTrends: (days = 30) => 
    apiClient.get('/analytics/deployment-trends', { params: { days } }),
  
  getTopRisks: (limit = 10) => 
    apiClient.get('/analytics/top-risks', { params: { limit } }),
  
  getChainStats: () => apiClient.get('/analytics/chain-stats'),
  
  getRiskFeed: (limit = 50) => 
    apiClient.get('/analytics/risk-feed', { params: { limit } }),
  
  getAnalyticsStats: () => apiClient.get('/analytics/stats'),
};