import React, { useState } from 'react';
import { TokenTable } from '../components/tokens/TokenTable';
import { TokenSearch } from '../components/tokens/TokenSearch';
import { Pagination } from '../components/common/Pagination';
import { Card } from '../components/common/Card';
import { useTokens, useInfiniteTokens } from '../hooks/useTokens';
import { usePagination } from '../hooks/usePagination';
import { Loading } from '../components/common/Loading';

export const Explorer = () => {
  const [filters, setFilters] = useState({});
  const { data: tokens, isLoading } = useTokens(filters);
  const { paginatedData, currentPage, setCurrentPage, totalPages } = usePagination(tokens, 20);

  const handleSearch = (query) => {
    setFilters(prev => ({ ...prev, search: query }));
  };

  const handleFilter = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Explorer</h1>
        <p className="text-primary-400 mt-1">
          Browse and analyze tokens deployed on Base
        </p>
      </div>

      <Card>
        <div className="space-y-6">
          <TokenSearch onSearch={handleSearch} onFilter={handleFilter} />
          <TokenTable tokens={paginatedData} />
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      </Card>
    </div>
  );
};