import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../common/Card';
import { RiskBadge } from '../risk/RiskBadge';
import { Badge } from '../common/Badge';
import { formatAddress, formatRelativeTime } from '../../services/utils/formatters';

export const TokenCard = ({ token, compact = false }) => {
  const navigate = useNavigate();

  return (
    <Card
      className="cursor-pointer hover:border-primary-600 transition-all"
      onClick={() => navigate(`/token/${token.address}`)}
    >
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <h3 className="font-medium">
              {token.name || 'Unknown Token'}
              {token.symbol && (
                <span className="text-primary-400 ml-2">${token.symbol}</span>
              )}
            </h3>
            <p className="font-mono text-xs text-primary-500 mt-1">
              {formatAddress(token.address)}
            </p>
          </div>
          <RiskBadge level={token.riskScore?.level} score={token.riskScore?.final} size="sm" />
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-xs text-primary-400">Deployer</p>
            <p className="font-mono text-sm mt-1">{formatAddress(token.deployer)}</p>
          </div>
          <div>
            <p className="text-xs text-primary-400">Deployed</p>
            <p className="text-sm mt-1">{formatRelativeTime(token.deployedAt)}</p>
          </div>
        </div>

        {/* Tags */}
        {!compact && (
          <div className="flex flex-wrap gap-2 pt-2">
            <Badge size="sm" variant={token.hasLiquidity ? 'success' : 'warning'}>
              {token.hasLiquidity ? 'Has Liquidity' : 'No Liquidity'}
            </Badge>
            <Badge size="sm" variant="info">
              {token.chain || 'Base'}
            </Badge>
            {(token.flags?.length > 0) && (
              <Badge size="sm" variant="error">
                {token.flags.length} Flags
              </Badge>
            )}
          </div>
        )}
      </div>
    </Card>
  );
};