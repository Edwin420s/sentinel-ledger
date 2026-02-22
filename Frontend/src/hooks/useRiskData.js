import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api/index';

export const useRiskFeed = (limit = 50) => {
  return useQuery({
    queryKey: ['risk-feed', limit],
    queryFn: () => api.getRiskFeed(limit),
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

export const useRiskDistribution = () => {
  return useQuery({
    queryKey: ['risk-distribution'],
    queryFn: () => api.getRiskDistribution(),
  });
};

export const useRiskTrends = (days = 7) => {
  return useQuery({
    queryKey: ['risk-trends', days],
    queryFn: () => api.getRiskTrends(days),
  });
};

export const useTopRisks = (limit = 10) => {
  return useQuery({
    queryKey: ['top-risks', limit],
    queryFn: () => api.getTopRisks(limit),
  });
};