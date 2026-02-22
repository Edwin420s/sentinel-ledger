import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = {
  LOW: '#22c55e',
  MODERATE: '#f59e0b',
  HIGH: '#f97316',
  CRITICAL: '#ef4444',
};

export const RiskDistributionChart = ({ data }) => {
  const chartData = data ? [
    { name: 'Low', value: data.low || 0, color: COLORS.LOW },
    { name: 'Moderate', value: data.moderate || 0, color: COLORS.MODERATE },
    { name: 'High', value: data.high || 0, color: COLORS.HIGH },
    { name: 'Critical', value: data.critical || 0, color: COLORS.CRITICAL },
  ].filter(item => item.value > 0) : [];

  if (chartData.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-primary-500">
        No data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={80}
          paddingAngle={2}
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: '#1e293b',
            border: '1px solid #334155',
            borderRadius: '0.5rem',
            color: '#f1f5f9',
          }}
        />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};