import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../common/Card';
import { RiskBadge } from '../risk/RiskBadge';
import { formatAddress, formatNumber } from '../../services/utils/formatters';
import { ExternalLink } from '../../assets/icons';

export const WalletCard = ({ wallet }) => {
  const navigate = useNavigate();

  return (
    <Card className="hover:border-primary-600 transition-colors cursor-pointer"
           onClick={() => navigate(`/wallet/${wallet.address}`)}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="font-mono text-sm">{formatAddress(wallet.address)}</p>
          <p className="text-xs text-primary-500 mt-1">
            First seen: {new Date(wallet.stats?.firstSeen).toLocaleDateString()}
          </p>
        </div>
        <RiskBadge level={wallet.riskScore ? 'HIGH' : 'LOW'} score={wallet.riskScore} size="sm" />
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm mb-4">
        <div>
          <p className="text-primary-400">Tokens Deployed</p>
          <p className="font-medium">{wallet.stats?.erc20Count || 0}</p>
        </div>
        <div>
          <p className="text-primary-400">Suspected Rugs</p>
          <p className="font-medium text-warning">{wallet.stats?.suspectedRugs || 0}</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs text-primary-500">
        <span>{wallet.chains?.join(', ')}</span>
        <ExternalLink className="w-4 h-4" />
      </div>
    </Card>
  );
};