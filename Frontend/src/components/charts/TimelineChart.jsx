import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';

export const TimelineChart = ({ data, dataKey = 'value', color = '#14b8a6' }) => {
  if (!data?.length) {
    return (
      <div className="h-64 flex items-center justify-center text-primary-500">
        No timeline data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis
          dataKey="timestamp"
          tickFormatter={(timestamp) => timestamp ? format(new Date(timestamp), 'MMM d') : ''}
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
          labelFormatter={(label) => label ? format(new Date(label), 'MMM d, yyyy HH:mm') : ''}
        />
        <Line
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 6, fill: color }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};