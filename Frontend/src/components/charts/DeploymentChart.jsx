import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format } from 'date-fns';

export const DeploymentChart = ({ data }) => {
  if (!data?.length) {
    return (
      <div className="h-64 flex items-center justify-center text-primary-500">
        No deployment data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis
          dataKey="date"
          tickFormatter={(date) => format(new Date(date), 'MMM d')}
          stroke="#94a3b8"
        />
        <YAxis stroke="#94a3b8" />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1e293b',
            border: '1px solid #334155',
            borderRadius: '0.5rem',
            color: '#f1f5f9',
          }}
          labelFormatter={(label) => format(new Date(label), 'MMM d, yyyy')}
        />
        <Bar dataKey="deployments" fill="#14b8a6" radius={[4, 4, 0, 0]} />
        <Bar dataKey="rugs" fill="#ef4444" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};