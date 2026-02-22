import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api/index';
import { Card } from '../components/common/Card';
import { TokenTable } from '../components/tokens/TokenTable';
import { RiskBadge } from '../components/risk/RiskBadge';
import { Loading } from '../components/common/Loading';
import { formatAddress, formatDate } from '../services/utils/formatters';
import { Copy, ExternalLink } from '../assets/icons';
import toast from 'react-hot-toast';

export const WalletDetail = () => {
  const { address } = useParams();

  const { data: wallet, isLoading } = useQuery({
    queryKey: ['wallet', address],
    queryFn: () => api.getWallet(address),
  });

  const { data: tokens } = useQuery({
    queryKey: ['wallet-tokens', address],
    queryFn: () => api.getWalletTokens(address),
  });

  const copyAddress = () => {
    navigator.clipboard.writeText(address);
    toast.success('Address copied to clipboard');
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Wallet Profile</h1>
          <div className="flex items-center space-x-2 mt-2">
            <span className="font-mono text-primary-400">{formatAddress(address, 8)}</span>
            <button onClick={copyAddress} className="text-primary-500 hover:text-primary-400">
              <Copy className="w-4 h-4" />
            </button>
            <a
              href={`https://basescan.org/address/${address}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent-light"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>
        <RiskBadge level={wallet?.riskScore > 50 ? 'HIGH' : 'LOW'} score={wallet?.riskScore} size="lg" />
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <p className="text-primary-400 text-sm">Total Contracts</p>
          <p className="text-2xl font-semibold mt-2">{wallet?.stats?.totalContracts || 0}</p>
        </Card>
        <Card>
          <p className="text-primary-400 text-sm">ERC20 Tokens</p>
          <p className="text-2xl font-semibold mt-2">{wallet?.stats?.erc20Count || 0}</p>
        </Card>
        <Card>
          <p className="text-primary-400 text-sm">Suspected Rugs</p>
          <p className="text-2xl font-semibold mt-2 text-warning">{wallet?.stats?.suspectedRugs || 0}</p>
        </Card>
        <Card>
          <p className="text-primary-400 text-sm">Wallet Age</p>
          <p className="text-2xl font-semibold mt-2">{wallet?.stats?.walletAgeDays || 0} days</p>
        </Card>
      </div>

      {/* Cross-chain Activity */}
      <Card title="Cross-Chain Activity">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium mb-4">Base</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-primary-400">Tokens Deployed</span>
                <span className="font-medium">{wallet?.crossChainActivity?.base?.tokensDeployed || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-primary-400">First Deployment</span>
                <span className="font-medium">
                  {wallet?.crossChainActivity?.base?.firstDeployment
                    ? formatDate(wallet.crossChainActivity.base.firstDeployment)
                    : 'Never'}
                </span>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-medium mb-4">Ethereum</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-primary-400">Tokens Deployed</span>
                <span className="font-medium">{wallet?.crossChainActivity?.ethereum?.tokensDeployed || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-primary-400">First Deployment</span>
                <span className="font-medium">
                  {wallet?.crossChainActivity?.ethereum?.firstDeployment
                    ? formatDate(wallet.crossChainActivity.ethereum.firstDeployment)
                    : 'Never'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Deployed Tokens */}
      <Card title="Deployed Tokens">
        <TokenTable tokens={tokens} showRiskBadge />
      </Card>
    </div>
  );
};