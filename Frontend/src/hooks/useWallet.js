import { useQuery } from '@tanstack/react-query';
import { api } from '../services';

export const useWallet = (address) => {
  return useQuery({
    queryKey: ['wallet', address],
    queryFn: () => api.getWallet(address),
    enabled: !!address,
  });
};

export const useWalletTokens = (address) => {
  return useQuery({
    queryKey: ['wallet-tokens', address],
    queryFn: () => api.getWalletTokens(address),
    enabled: !!address,
  });
};

export const useWalletTransactions = (address, limit = 10) => {
  return useQuery({
    queryKey: ['wallet-transactions', address, limit],
    queryFn: () => api.getWalletTransactions(address, limit),
    enabled: !!address,
  });
};

export const useWalletGraph = (address) => {
  return useQuery({
    queryKey: ['wallet-graph', address],
    queryFn: () => api.getWalletGraph(address),
    enabled: !!address,
  });
};