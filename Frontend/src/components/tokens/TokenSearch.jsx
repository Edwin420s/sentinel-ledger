import React, { useState } from 'react';
import { Search, Filter } from '../../assets/icons';
import { Input } from '../common/Input';
import { Button } from '../common/Button';
import { useDebounce } from '../../hooks/useDebounce';

export const TokenSearch = ({ onSearch, onFilter }) => {
  const [query, setQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    minRisk: '',
    maxRisk: '',
    chain: '',
    hasLiquidity: '',
  });

  const debouncedSearch = useDebounce(query, 300);

  React.useEffect(() => {
    onSearch(debouncedSearch);
  }, [debouncedSearch, onSearch, query]); // Added query to the dependencies array

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilter(newFilters);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <div className="flex-1">
          <Input
            placeholder="Search by token address or name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            icon={Search}
          />
        </div>
        <Button
          variant={showFilters ? 'primary' : 'outline'}
          onClick={() => setShowFilters(!showFilters)}
          icon={Filter}
        >
          Filters
        </Button>
      </div>

      {showFilters && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 bg-primary-800/30 rounded-lg">
          <Input
            label="Min Risk"
            type="number"
            placeholder="0"
            value={filters.minRisk}
            onChange={(e) => handleFilterChange('minRisk', e.target.value)}
          />
          <Input
            label="Max Risk"
            type="number"
            placeholder="100"
            value={filters.maxRisk}
            onChange={(e) => handleFilterChange('maxRisk', e.target.value)}
          />
          <div className="space-y-1">
            <label className="text-sm text-primary-400">Chain</label>
            <select
              className="w-full bg-primary-800 border border-primary-700 rounded-lg px-4 py-2 text-primary-100"
              value={filters.chain}
              onChange={(e) => handleFilterChange('chain', e.target.value)}
            >
              <option value="">All</option>
              <option value="base">Base</option>
              <option value="ethereum">Ethereum</option>
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-sm text-primary-400">Liquidity</label>
            <select
              className="w-full bg-primary-800 border border-primary-700 rounded-lg px-4 py-2 text-primary-100"
              value={filters.hasLiquidity}
              onChange={(e) => handleFilterChange('hasLiquidity', e.target.value)}
            >
              <option value="">All</option>
              <option value="true">Has Liquidity</option>
              <option value="false">No Liquidity</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
};