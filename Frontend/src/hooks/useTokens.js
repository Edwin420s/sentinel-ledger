import { useQuery, useInfiniteQuery } from '@tanstack/react-query';
import { api } from '../services';

export const useTokens = (filters = {}) => {
  return useQuery({
    queryKey: ['tokens', filters],
    queryFn: () => api.getTokens(filters),
    select: (response) => {
      // Handle different response formats
      if (Array.isArray(response)) {
        return response;
      }
      if (response && response.tokens && Array.isArray(response.tokens)) {
        return response.tokens;
      }
      if (response && response.data && Array.isArray(response.data)) {
        return response.data;
      }
      // Fallback to empty array
      return [];
    },
  });
};

export const useInfiniteTokens = (filters = {}) => {
  return useInfiniteQuery({
    queryKey: ['infiniteTokens', filters],
    queryFn: ({ pageParam = 1 }) => api.getTokens({ ...filters, page: pageParam }),
    select: (response) => {
      // Handle different response formats
      if (Array.isArray(response)) {
        return response;
      }
      if (response && response.tokens && Array.isArray(response.tokens)) {
        return response.tokens;
      }
      if (response && response.data && Array.isArray(response.data)) {
        return response.data;
      }
      // Fallback to empty array
      return [];
    },
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