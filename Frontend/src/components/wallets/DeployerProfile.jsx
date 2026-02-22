import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { api } from '../../services/api/client';
import { formatAddress } from '../../services/utils/formatters';
import { User, ExternalLink } from '../../assets/icons';

export const DeployerProfile = ({ deployer }) => {
  const navigate = useNavigate();
  
  const { data: wallet, isLoading } = useQuery({
    queryKey: ['wallet', deployer],
    queryFn: () => api.getWallet(deployer),
    enabled: !!deployer,
  });

  if (isLoading) {
    return (
      <Card title="Deployer Profile">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-primary-700 rounded w-3/4"></div>
          <div className="h-4 bg-primary-700 rounded w-1/2"></div>
        </div>
      </Card>
    );
  }

  return (
    <Card title="Deployer Profile">
      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-primary-700/30 rounded-full">
            <User className="w-5 h-5 text-accent" />
          </div>
          <div className="flex-1">
            <p className="font-mono text-sm">{formatAddress(deployer)}</p>
            <p className="text-xs text-primary-500">
              Active on {wallet?.chains?.join(', ')}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-primary-400">Total Contracts</p>
            <p className="font-medium mt-1">{wallet?.stats?.totalContracts || 0}</p>
          </div>
          <div>
            <p className="text-primary-400">ERC20 Tokens</p>
            <p className="font-medium mt-1">{wallet?.stats?.erc20Count || 0}</p>
          </div>
          <div>
            <p className="text-primary-400">Suspected Rugs</p>
            <p className="font-medium mt-1 text-warning">{wallet?.stats?.suspectedRugs || 0}</p>
          </div>
          <div>
            <p className="text-primary-400">Wallet Age</p>
            <p className="font-medium mt-1">{wallet?.stats?.walletAgeDays || 0} days</p>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          className="w-full"
          onClick={() => navigate(`/wallet/${deployer}`)}
        >
          View Full Profile
        </Button>
      </div>
    </Card>
  );
};