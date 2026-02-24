import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { TokenTable } from '../components/tokens/TokenTable';
import { RiskDistributionChart } from '../components/charts/RiskDistributionChart';
import { TimelineChart } from '../components/charts/TimelineChart';
import { Card } from '../components/common/Card';
import { api } from '../services';
import { Loading } from '../components/common/Loading';
import { Shield, Activity, AlertTriangle, Wallet } from '../assets/icons';
import ApiTest from '../components/test/ApiTest';

export const Dashboard = () => {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => api.getDashboardStats(),
  });

  const { data: recentTokens, isLoading: tokensLoading } = useQuery({
    queryKey: ['recent-tokens'],
    queryFn: () => api.getRecentTokens(10),
  });

  const { data: highRiskTokens, isLoading: highRiskLoading } = useQuery({
    queryKey: ['high-risk-tokens'],
    queryFn: () => api.getHighRiskTokens(5),
  });

  const { data: trends } = useQuery({
    queryKey: ['deployment-trends-dashboard'],
    queryFn: () => api.getDeploymentTrends(7),
  });

  if (statsLoading || tokensLoading || highRiskLoading) {
    return <Loading />;
  }

  const metrics = [
    {
      label: 'Total Tokens Indexed',
      value: stats?.totalTokens || 0,
      icon: Activity,
      change: '+12%',
    },
    {
      label: 'High Risk Detected',
      value: stats?.highRiskCount || 0,
      icon: AlertTriangle,
      change: stats?.highRiskPercentage || '0%',
    },
    {
      label: 'Active Deployers',
      value: stats?.activeDeployers || 0,
      icon: Wallet,
      change: '+5%',
    },
    {
      label: 'Total Flags',
      value: stats?.totalFlags || 0,
      icon: Shield,
      change: stats?.newFlags || '0',
    },
  ];

  return (
    <div className="space-y-6">
      {/* API Test Component - Development Only */}
      {process.env.NODE_ENV === 'development' && <ApiTest />}

      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold">Dashboard</h1>
        <p className="text-primary-400 mt-1">
          Real-time risk intelligence for Base ecosystem
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric) => (
          <Card key={metric.label} className="relative overflow-hidden">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-primary-400 text-sm">{metric.label}</p>
                <p className="text-3xl font-semibold mt-2">{metric.value}</p>
                <p className="text-xs text-primary-500 mt-1">
                  {metric.change} from yesterday
                </p>
              </div>
              <div className="p-3 bg-primary-700/30 rounded-lg">
                <metric.icon className="w-6 h-6 text-accent" />
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Risk Distribution">
          <RiskDistributionChart data={stats?.riskDistribution} />
        </Card>
        <Card title="Recent Activity">
          <TimelineChart
            data={trends?.timeline || []}
            dataKey="deployments"
            color="#14b8a6"
          />
        </Card>
      </div>

      {/* Token Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Recently Deployed">
          <TokenTable
            tokens={recentTokens}
            showRiskBadge
            compact
          />
        </Card>

        <Card title="High Risk Tokens">
          <TokenTable
            tokens={highRiskTokens}
            showRiskBadge
            compact
          />
        </Card>
      </div>
    </div>
  );
};