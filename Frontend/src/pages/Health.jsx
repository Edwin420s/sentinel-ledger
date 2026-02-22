import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { api } from '../services/api/index';
import { CheckCircle, XCircle, Activity } from '../assets/icons';

export const Health = () => {
  const { data: health, isLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => api.get('/health'),
    refetchInterval: 10000, // Check every 10 seconds
  });

  const services = [
    { name: 'API Server', status: health?.api?.status },
    { name: 'Database', status: health?.database?.status },
    { name: 'Indexer', status: health?.indexer?.status },
    { name: 'WebSocket', status: health?.websocket?.status },
    { name: 'Blockchain RPC', status: health?.rpc?.status },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">System Health</h1>
        <p className="text-primary-400 mt-1">
          Monitor platform status and performance
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Uptime Card */}
        <Card className="col-span-1">
          <div className="flex items-center space-x-3">
            <Activity className="w-8 h-8 text-accent" />
            <div>
              <p className="text-primary-400 text-sm">Uptime</p>
              <p className="text-2xl font-semibold">{health?.uptime || '99.9%'}</p>
            </div>
          </div>
        </Card>

        {/* Version Card */}
        <Card className="col-span-1">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-accent/20 rounded-full flex items-center justify-center">
              <span className="text-accent font-mono">v1</span>
            </div>
            <div>
              <p className="text-primary-400 text-sm">Version</p>
              <p className="text-2xl font-semibold">{health?.version || '1.0.0'}</p>
            </div>
          </div>
        </Card>

        {/* Last Block Card */}
        <Card className="col-span-1">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-700 rounded-full flex items-center justify-center">
              <span className="text-primary-300">#</span>
            </div>
            <div>
              <p className="text-primary-400 text-sm">Last Block</p>
              <p className="text-2xl font-semibold">{health?.lastBlock || '0'}</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Services Status */}
      <Card title="Services Status">
        <div className="space-y-4">
          {services.map((service) => (
            <div key={service.name} className="flex items-center justify-between py-2">
              <span className="text-primary-300">{service.name}</span>
              <div className="flex items-center space-x-3">
                {service.status === 'healthy' ? (
                  <>
                    <CheckCircle className="w-5 h-5 text-success" />
                    <Badge variant="success">Operational</Badge>
                  </>
                ) : service.status === 'degraded' ? (
                  <>
                    <Activity className="w-5 h-5 text-warning" />
                    <Badge variant="warning">Degraded</Badge>
                  </>
                ) : (
                  <>
                    <XCircle className="w-5 h-5 text-error" />
                    <Badge variant="error">Down</Badge>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Performance Metrics */}
      <Card title="Performance Metrics">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-primary-400 text-sm mb-4">Response Times</p>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm">API Average</span>
                <span className="font-mono">{health?.metrics?.apiAvg || '120'}ms</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Database Query</span>
                <span className="font-mono">{health?.metrics?.dbAvg || '45'}ms</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">RPC Request</span>
                <span className="font-mono">{health?.metrics?.rpcAvg || '230'}ms</span>
              </div>
            </div>
          </div>
          <div>
            <p className="text-primary-400 text-sm mb-4">Request Volume</p>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm">Last Hour</span>
                <span className="font-mono">{health?.metrics?.requests1h || '1.2k'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Last 24h</span>
                <span className="font-mono">{health?.metrics?.requests24h || '28.5k'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Peak</span>
                <span className="font-mono">{health?.metrics?.peakRequests || '180/min'}</span>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};