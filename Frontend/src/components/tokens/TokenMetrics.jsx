import React from 'react';
import { Card } from '../common/Card';
import { Tooltip } from '../common/Tooltip';
import { formatNumber, formatCurrency } from '../../services/utils/formatters';
import { TrendingUp, TrendingDown, Minus } from '../../assets/icons';

export const TokenMetrics = ({ token }) => {
  const metrics = [
    {
      label: 'Total Supply',
      value: token.totalSupply ? formatNumber(token.totalSupply) : 'Unknown',
      tooltip: 'Total token supply',
    },
    {
      label: 'Holder Count',
      value: token.holderCount ? formatNumber(token.holderCount) : 'Unknown',
      tooltip: 'Number of token holders',
    },
    {
      label: 'Transfer Count',
      value: token.transferCount ? formatNumber(token.transferCount) : 'Unknown',
      tooltip: 'Total number of transfers',
    },
    {
      label: 'Market Cap',
      value: token.marketCap ? formatCurrency(token.marketCap) : 'Unknown',
      tooltip: 'Fully diluted market cap',
    },
  ];

  const getTrendIcon = (trend) => {
    if (trend > 0) return <TrendingUp className="w-4 h-4 text-success" />;
    if (trend < 0) return <TrendingDown className="w-4 h-4 text-error" />;
    return <Minus className="w-4 h-4 text-primary-500" />;
  };

  return (
    <Card title="Token Metrics">
      <div className="grid grid-cols-2 gap-4">
        {metrics.map((metric) => (
          <div key={metric.label}>
            <div className="flex items-center space-x-1 mb-1">
              <span className="text-xs text-primary-400">{metric.label}</span>
              <Tooltip content={metric.tooltip}>
                <span className="text-primary-500 cursor-help text-xs">ⓘ</span>
              </Tooltip>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium">{metric.value}</span>
              {metric.trend !== undefined && getTrendIcon(metric.trend)}
            </div>
          </div>
        ))}
      </div>

      {/* Price Chart Link */}
      {token.priceData && (
        <div className="mt-4 pt-4 border-t border-primary-700">
          <a
            href={token.priceData.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between text-sm text-accent hover:text-accent-light"
          >
            <span>View price chart</span>
            <span>→</span>
          </a>
        </div>
      )}
    </Card>
  );
};