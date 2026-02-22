import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card } from '../components/common/Card';
import { RiskDistributionChart } from '../components/charts/RiskDistributionChart';
import { DeploymentChart } from '../components/charts/DeploymentChart';
import { TimelineChart } from '../components/charts/TimelineChart';
import { Select } from '../components/common/Select';
import { Loading } from '../components/common/Loading';
import { api } from '../services';
import { formatNumber } from '../services/utils/formatters';

export const Analytics = () => {
  const [timeframe, setTimeframe] = React.useState('7d');

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['analytics-stats'],
    queryFn: () => api.getAnalyticsStats(),
  });

  const { data: trends, isLoading: trendsLoading } = useQuery({
    queryKey: ['risk-trends', timeframe],
    queryFn: () => api.getRiskTrends(timeframe),
  });

  const { data: distribution, isLoading: distLoading } = useQuery({
    queryKey: ['risk-distribution'],
    queryFn: () => api.getRiskDistribution(),
  });

  const timeframeOptions = [
    { value: '24h', label: 'Last 24 Hours' },
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: '90d', label: 'Last 90 Days' },
  ];

  if (statsLoading || trendsLoading || distLoading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Analytics</h1>
          <p className="text-primary-400 mt-1">
            Platform statistics and trends
          </p>
        </div>
        <Select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          options={timeframeOptions}
          className="w-48"
        />
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <p className="text-primary-400 text-sm">Total Tokens</p>
          <p className="text-2xl font-semibold mt-2">{formatNumber(stats?.totalTokens || 0)}</p>
          <p className="text-xs text-success mt-1">↑ 12% from last month</p>
        </Card>
        <Card>
          <p className="text-primary-400 text-sm">Total Deployers</p>
          <p className="text-2xl font-semibold mt-2">{formatNumber(stats?.totalDeployers || 0)}</p>
          <p className="text-xs text-success mt-1">↑ 8% from last month</p>
        </Card>
        <Card>
          <p className="text-primary-400 text-sm">Rugs Detected</p>
          <p className="text-2xl font-semibold mt-2 text-warning">{formatNumber(stats?.totalRugs || 0)}</p>
          <p className="text-xs text-error mt-1">↑ 5% from last month</p>
        </Card>
        <Card>
          <p className="text-primary-400 text-sm">Avg. Risk Score</p>
          <p className="text-2xl font-semibold mt-2">{stats?.avgRiskScore || 0}</p>
          <p className="text-xs text-warning mt-1">Moderate risk level</p>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Risk Distribution">
          <RiskDistributionChart data={distribution} />
        </Card>

        <Card title="Deployment Trends">
          <DeploymentChart data={trends?.deployments} />
        </Card>
      </div>

      {/* Timeline */}
      <Card title="Risk Score Timeline">
        <TimelineChart
          data={trends?.timeline}
          dataKey="avgRiskScore"
          color="#14b8a6"
        />
      </Card>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Top Risk Factors">
          <div className="space-y-3">
            {stats?.topRiskFactors?.map((factor, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-primary-300">{factor.name}</span>
                <span className="text-sm font-medium">{factor.count}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Most Active Chains">
          <div className="space-y-3">
            {stats?.chainActivity?.map((chain, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-primary-300 capitalize">{chain.name}</span>
                <span className="text-sm font-medium">{chain.count} tokens</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Recent Alerts">
          <div className="space-y-3">
            {stats?.recentAlerts?.map((alert, index) => (
              <div key={index} className="text-sm">
                <span className="text-warning">⚠️</span>
                <span className="text-primary-300 ml-2">{alert.message}</span>
                <p className="text-xs text-primary-500 mt-1">{alert.time}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};