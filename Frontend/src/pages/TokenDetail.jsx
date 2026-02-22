import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api/client';
import { RiskBadge } from '../components/risk/RiskBadge';
import { ScoreBreakdown } from '../components/risk/ScoreBreakdown';
import { FlagList } from '../components/risk/FlagList';
import { LiquidityCard } from '../components/liquidity/LiquidityCard';
import { DeployerProfile } from '../components/wallets/DeployerProfile';
import { Card } from '../components/common/Card';
import { Loading } from '../components/common/Loading';
import { formatRelativeTime } from '../services/utils/formatters';
import { Shield, Calendar, User, Hash } from '../assets/icons';

export const TokenDetail = () => {
  const { address } = useParams();
  
  const { data: token, isLoading } = useQuery({
    queryKey: ['token', address],
    queryFn: () => api.getToken(address),
  });

  if (isLoading) {
    return <Loading />;
  }

  if (!token) {
    return (
      <div className="py-12 text-center text-primary-500">
        Token not found
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold">
            {token.name || 'Token'} 
            {token.symbol && <span className="text-primary-400 ml-2">${token.symbol}</span>}
          </h1>
          <div className="flex items-center space-x-4 mt-2">
            <div className="flex items-center space-x-2 text-primary-400">
              <Hash className="w-4 h-4" />
              <span className="font-mono text-sm">{token.address}</span>
            </div>
            <div className="flex items-center space-x-2 text-primary-400">
              <Calendar className="w-4 h-4" />
              <span className="text-sm">
                {formatRelativeTime(token.deployedAt)}
              </span>
            </div>
            <div className="flex items-center space-x-2 text-primary-400">
              <User className="w-4 h-4" />
              <span className="font-mono text-sm">
                {token.deployer?.slice(0, 6)}...{token.deployer?.slice(-4)}
              </span>
            </div>
          </div>
        </div>
        
        <RiskBadge level={token.riskScore?.level} score={token.riskScore?.final} size="lg" />
      </div>

      {/* AI Explanation */}
      <Card className="border-accent/20 bg-accent/5">
        <div className="flex items-start space-x-3">
          <Shield className="w-5 h-5 text-accent flex-shrink-0 mt-1" />
          <div>
            <h3 className="font-medium mb-2">AI Risk Analysis</h3>
            <p className="text-primary-300 leading-relaxed">
              {token.aiExplanation}
            </p>
          </div>
        </div>
      </Card>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ScoreBreakdown scores={token.riskScore} />
          <FlagList flags={token.flags} />
        </div>

        <div className="space-y-6">
          <LiquidityCard pools={token.liquidityPools} />
          <DeployerProfile deployer={token.deployer} />
        </div>
      </div>

      {/* Token Metrics */}
      <Card title="Token Details">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <p className="text-primary-400 text-sm">Chain</p>
            <p className="font-medium mt-1 capitalize">{token.chain}</p>
          </div>
          <div>
            <p className="text-primary-400 text-sm">Total Supply</p>
            <p className="font-mono mt-1">{token.totalSupply || 'Unknown'}</p>
          </div>
          <div>
            <p className="text-primary-400 text-sm">Deployed Block</p>
            <p className="font-mono mt-1">{token.deployedBlock}</p>
          </div>
          <div>
            <p className="text-primary-400 text-sm">Deployer Tokens</p>
            <p className="font-mono mt-1">12 (3 high risk)</p>
          </div>
        </div>
      </Card>
    </div>
  );
};