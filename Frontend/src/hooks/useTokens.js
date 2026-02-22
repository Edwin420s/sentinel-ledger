import { useQuery, useInfiniteQuery } from '@tanstack/react-query';
import { api } from '../services';

export const useTokens = (filters = {}) => {
  return useQuery({
    queryKey: ['tokens', filters],
    queryFn: () => api.getTokens(filters),
  });
};

export const useInfiniteTokens = (filters = {}) => {
  return useInfiniteQuery({
    queryKey: ['infiniteTokens', filters],
    queryFn: ({ pageParam = 1 }) => api.getTokens({ ...filters, page: pageParam }),
    getNextPageParam: (lastPage, pages) => {
      if (lastPage.length < 20) return undefined;
      return pages.length + 1;
    },
  });
};

export const useToken = (address) => {
  return useQuery({
    queryKey: ['token', address],
    queryFn: () => api.getToken(address),
    enabled: !!address,
  });
};