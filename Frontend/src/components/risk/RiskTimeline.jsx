import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card } from '../common/Card';
import { format } from 'date-fns';

export const RiskTimeline = ({ data, title = 'Risk Score Timeline' }) => {
  if (!data?.length) {
    return (
      <Card title={title}>
        <div className="h-64 flex items-center justify-center text-primary-500">
          No timeline data available
        </div>
      </Card>
    );
  }

  return (
    <Card title={title}>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(timestamp) => format(new Date(timestamp), 'MMM d')}
            stroke="#94a3b8"
          />
          <YAxis domain={[0, 100]} stroke="#94a3b8" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              color: '#f1f5f9',
            }}
            labelFormatter={(label) => format(new Date(label), 'MMM d, yyyy HH:mm')}
            formatter={(value) => [`${value}`, 'Risk Score']}
          />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#14b8a6"
            strokeWidth={2}
            dot={{ fill: '#14b8a6', r: 4 }}
            activeDot={{ r: 6, fill: '#14b8a6' }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      {/* Threshold lines */}
      <div className="mt-4 grid grid-cols-4 gap-2 text-xs">
        <div className="text-center">
          <div className="h-1 bg-risk-low rounded mb-1"></div>
          <span className="text-primary-400">Low (&lt;30)</span>
        </div>
        <div className="text-center">
          <div className="h-1 bg-risk-moderate rounded mb-1"></div>
          <span className="text-primary-400">Moderate (30-60)</span>
        </div>
        <div className="text-center">
          <div className="h-1 bg-risk-high rounded mb-1"></div>
          <span className="text-primary-400">High (60-80)</span>
        </div>
        <div className="text-center">
          <div className="h-1 bg-risk-critical rounded mb-1"></div>
          <span className="text-primary-400">Critical (&gt;80)</span>
        </div>
      </div>
    </Card>
  );
};