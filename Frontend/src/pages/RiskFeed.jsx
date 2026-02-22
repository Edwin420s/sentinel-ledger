import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../services';
import { Card } from '../components/common/Card';
import { RiskBadge } from '../components/risk/RiskBadge';
import { Button } from '../components/common/Button';
import { Loading } from '../components/common/Loading';
import { formatRelativeTime, formatAddress } from '../services/utils/formatters';
import { Refresh, AlertTriangle, Shield, Activity } from '../assets/icons';
import toast from 'react-hot-toast';

export const RiskFeed = () => {
    const navigate = useNavigate();

    const { data: events, isLoading, refetch, isRefetching } = useQuery({
        queryKey: ['risk-feed'],
        queryFn: () => api.getRiskFeed(),
        refetchInterval: 30000, // Refetch every 30 seconds
    });

    const handleRefresh = () => {
        refetch();
        toast.success('Feed updated');
    };

    const getEventIcon = (type) => {
        switch (type) {
            case 'high_risk':
                return <AlertTriangle className="w-5 h-5 text-error" />;
            case 'new_token':
                return <Activity className="w-5 h-5 text-info" />;
            case 'rug_detected':
                return <Shield className="w-5 h-5 text-warning" />;
            default:
                return <Activity className="w-5 h-5 text-primary-400" />;
        }
    };

    if (isLoading) {
        return <Loading />;
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-semibold">Risk Feed</h1>
                    <p className="text-primary-400 mt-1">
                        Real-time alerts and risk events
                    </p>
                </div>
                <Button
                    variant="outline"
                    onClick={handleRefresh}
                    loading={isRefetching}
                    icon={Refresh}
                >
                    Refresh
                </Button>
            </div>

            <div className="space-y-4">
                {events?.length === 0 ? (
                    <Card>
                        <div className="py-12 text-center text-primary-500">
                            No events in the feed
                        </div>
                    </Card>
                ) : (
                    events?.map((event) => (
                        <Card
                            key={event.id}
                            className="hover:border-primary-600 transition-colors cursor-pointer"
                            onClick={() => navigate(`/token/${event.tokenAddress}`)}
                        >
                            <div className="flex items-start space-x-4">
                                <div className="p-2 bg-primary-700/30 rounded-lg flex-shrink-0">
                                    {getEventIcon(event.type)}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center justify-between flex-wrap gap-2">
                                        <div className="flex items-center space-x-3">
                                            <h3 className="font-medium">{event.title}</h3>
                                            <RiskBadge level={event.riskLevel} score={event.riskScore} size="sm" />
                                        </div>
                                        <span className="text-xs text-primary-500">
                                            {formatRelativeTime(event.timestamp)}
                                        </span>
                                    </div>
                                    <p className="text-sm text-primary-300 mt-1">{event.description}</p>
                                    <div className="flex items-center space-x-4 mt-3 text-xs">
                                        <span className="font-mono text-primary-500">
                                            {formatAddress(event.tokenAddress)}
                                        </span>
                                        <span className="text-primary-600">•</span>
                                        <span className="text-primary-500">
                                            Deployer: {formatAddress(event.deployer)}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
};
