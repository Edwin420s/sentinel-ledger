import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services';
import { Card } from '../common/Card';
import { RiskBadge } from './RiskBadge';
import { Button } from '../common/Button';
import { formatRelativeTime, formatAddress } from '../../services/utils/formatters';
import { Refresh, AlertTriangle, Shield, Activity } from '../../assets/icons';
import toast from 'react-hot-toast';

// This component can be embedded inline on any page for a compact risk feed widget.
// The full page version lives at src/pages/RiskFeed.jsx
export const RiskFeedWidget = ({ limit = 10 }) => {
  const navigate = useNavigate();

  const { data: events, isLoading, refetch, isRefetching } = useQuery({
    queryKey: ['risk-feed-widget', limit],
    queryFn: () => api.getRiskFeed(limit),
    refetchInterval: 30000,
  });

  const handleRefresh = () => {
    refetch();
    toast.success('Feed updated');
  };

  const getEventIcon = (type) => {
    switch (type) {
      case 'high_risk':
        return <AlertTriangle className="w-4 h-4 text-error" />;
      case 'new_token':
        return <Activity className="w-4 h-4 text-info" />;
      case 'rug_detected':
        return <Shield className="w-4 h-4 text-warning" />;
      default:
        return <Activity className="w-4 h-4 text-primary-400" />;
    }
  };

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-medium">Live Risk Feed</h3>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleRefresh}
          loading={isRefetching}
          icon={Refresh}
        />
      </div>

      <div className="space-y-3">
        {isLoading ? (
          <div className="py-6 text-center text-primary-500 text-sm">Loading...</div>
        ) : events?.length === 0 ? (
          <div className="py-6 text-center text-primary-500 text-sm">No events yet</div>
        ) : (
          events?.slice(0, limit).map((event) => (
            <div
              key={event.id}
              className="flex items-start space-x-3 p-3 rounded-lg bg-primary-700/20 hover:bg-primary-700/40 cursor-pointer transition-colors"
              onClick={() => navigate(`/token/${event.tokenAddress}`)}
            >
              <div className="mt-0.5 flex-shrink-0">
                {getEventIcon(event.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium truncate">{event.title}</span>
                  <RiskBadge level={event.riskLevel} size="sm" />
                </div>
                <p className="text-xs text-primary-400 mt-0.5 truncate">{event.description}</p>
                <span className="text-xs text-primary-500">{formatRelativeTime(event.timestamp)}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </Card>
  );
};

// Keep backward-compat default export
export default RiskFeedWidget;