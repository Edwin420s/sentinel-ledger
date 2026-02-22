import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { ZoomIn, ZoomOut, RefreshCw } from '../../assets/icons';

export const WalletGraph = ({ graphData }) => {
  const [zoom, setZoom] = React.useState(1);

  if (!graphData || graphData.nodes?.length === 0) {
    return (
      <Card title="Wallet Relationship Graph">
        <div className="h-96 flex items-center justify-center text-primary-500">
          No relationship data available
        </div>
      </Card>
    );
  }

  return (
    <Card title="Wallet Relationship Graph">
      <div className="space-y-4">
        {/* Graph Controls */}
        <div className="flex items-center justify-end space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setZoom(Math.min(zoom + 0.1, 2))}
            icon={ZoomIn}
            disabled={zoom >= 2}
          />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setZoom(Math.max(zoom - 0.1, 0.5))}
            icon={ZoomOut}
            disabled={zoom <= 0.5}
          />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setZoom(1)}
            icon={RefreshCw}
          />
        </div>

        {/* Graph Visualization Placeholder */}
        <div 
          className="h-96 bg-primary-800/30 rounded-lg border border-primary-700 relative overflow-hidden"
          style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }}
        >
          {/* This is a placeholder for actual graph visualization */}
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-primary-500">
              Graph visualization coming soon
              <br />
              <span className="text-xs">
                Nodes: {graphData.nodes?.length || 0}, 
                Edges: {graphData.edges?.length || 0}
              </span>
            </p>
          </div>

          {/* Simple node representation */}
          <svg className="absolute inset-0 w-full h-full">
            {graphData.edges?.map((edge, i) => (
              <line
                key={i}
                x1="50%"
                y1="50%"
                x2="70%"
                y2="30%"
                stroke="#334155"
                strokeWidth="1"
                strokeDasharray="5,5"
              />
            ))}
            {graphData.nodes?.map((node, i) => (
              <circle
                key={i}
                cx={`${30 + (i * 20)}%`}
                cy="50%"
                r="10"
                fill={node.riskLevel === 'HIGH' ? '#ef4444' : '#14b8a6'}
                opacity="0.5"
              />
            ))}
          </svg>
        </div>

        {/* Legend */}
        <div className="flex items-center space-x-6 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-accent"></div>
            <span className="text-primary-400">Low Risk Wallet</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-error"></div>
            <span className="text-primary-400">High Risk Wallet</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 border border-dashed border-primary-600"></div>
            <span className="text-primary-400">Transaction</span>
          </div>
        </div>
      </div>
    </Card>
  );
};