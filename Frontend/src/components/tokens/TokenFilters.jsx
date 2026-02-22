import React from 'react';
import { Card } from '../common/Card';
import { Input } from '../common/Input';
import { Select } from '../common/Select';
import { Button } from '../common/Button';
import { Filter, X } from '../../assets/icons';

const riskLevels = [
  { value: '', label: 'All Levels' },
  { value: 'LOW', label: 'Low' },
  { value: 'MODERATE', label: 'Moderate' },
  { value: 'HIGH', label: 'High' },
  { value: 'CRITICAL', label: 'Critical' },
];

const chains = [
  { value: '', label: 'All Chains' },
  { value: 'base', label: 'Base' },
  { value: 'ethereum', label: 'Ethereum' },
];

const sortOptions = [
  { value: 'newest', label: 'Newest First' },
  { value: 'oldest', label: 'Oldest First' },
  { value: 'risk_high', label: 'Highest Risk' },
  { value: 'risk_low', label: 'Lowest Risk' },
];

export const TokenFilters = ({ filters, onChange, onReset }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const handleChange = (key, value) => {
    onChange({ ...filters, [key]: value });
  };

  const hasActiveFilters = Object.values(filters).some(v => v !== '' && v !== undefined);

  return (
    <div className="space-y-4">
      {/* Mobile Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden flex items-center space-x-2 text-primary-400 hover:text-primary-200"
      >
        <Filter className="w-5 h-5" />
        <span>Filters {hasActiveFilters && '(Active)'}</span>
      </button>

      {/* Filters Content */}
      <div className={`${isOpen ? 'block' : 'hidden lg:block'}`}>
        <Card className="p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium">Filters</h3>
            {hasActiveFilters && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onReset}
                icon={X}
                className="text-primary-400"
              >
                Reset
              </Button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Select
              label="Risk Level"
              value={filters.riskLevel || ''}
              onChange={(e) => handleChange('riskLevel', e.target.value)}
              options={riskLevels}
            />

            <Select
              label="Chain"
              value={filters.chain || ''}
              onChange={(e) => handleChange('chain', e.target.value)}
              options={chains}
            />

            <Select
              label="Sort By"
              value={filters.sortBy || 'newest'}
              onChange={(e) => handleChange('sortBy', e.target.value)}
              options={sortOptions}
            />

            <div className="space-y-1">
              <label className="text-sm text-primary-400">Min. Liquidity</label>
              <Input
                type="number"
                placeholder="USD"
                value={filters.minLiquidity || ''}
                onChange={(e) => handleChange('minLiquidity', e.target.value)}
              />
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-primary-700">
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  className="form-checkbox bg-primary-700 border-primary-600 rounded"
                  checked={filters.hasLiquidity || false}
                  onChange={(e) => handleChange('hasLiquidity', e.target.checked)}
                />
                <span className="text-sm text-primary-300">Has Liquidity</span>
              </label>

              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  className="form-checkbox bg-primary-700 border-primary-600 rounded"
                  checked={filters.hasFlags || false}
                  onChange={(e) => handleChange('hasFlags', e.target.checked)}
                />
                <span className="text-sm text-primary-300">Has Risk Flags</span>
              </label>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};