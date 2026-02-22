import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card } from '../common/Card';
import { formatCurrency } from '../../services/utils/formatters';

export const PoolChart = ({ data, poolAddress }) => {
  if (!data?.length) {
    return (
      <Card title="Liquidity History">
        <div className="h-64 flex items-center justify-center text-primary-500">
          No liquidity history available
        </div>
      </Card>
    );
  }

  return (
    <Card title="Liquidity History">
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(timestamp) => new Date(timestamp).toLocaleDateString()}
            stroke="#94a3b8"
          />
          <YAxis
            tickFormatter={(value) => `$${value.toLocaleString()}`}
            stroke="#94a3b8"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              color: '#f1f5f9',
            }}
            formatter={(value) => [formatCurrency(value), 'Liquidity']}
            labelFormatter={(label) => new Date(label).toLocaleString()}
          />
          <Area
            type="monotone"
            dataKey="liquidity"
            stroke="#14b8a6"
            fill="#14b8a6"
            fillOpacity={0.2}
          />
        </AreaChart>
      </ResponsiveContainer>
      
      {poolAddress && (
        <div className="mt-4 text-xs text-primary-500 text-center">
          Pool: {poolAddress.slice(0, 10)}...{poolAddress.slice(-8)}
        </div>
      )}
    </Card>
  );
};