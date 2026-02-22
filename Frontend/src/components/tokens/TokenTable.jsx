import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Table } from '../common/Table';
import { RiskBadge } from '../risk/RiskBadge';
import { formatAddress, formatRelativeTime } from '../../services/utils/formatters';

export const TokenTable = ({ tokens, showRiskBadge = true, compact = false }) => {
  const navigate = useNavigate();

  const columns = [
    {
      key: 'address',
      label: 'Token',
      render: (value, row) => (
        <div>
          <div className="font-mono">{formatAddress(value)}</div>
          {row.symbol && (
            <div className="text-xs text-primary-500">{row.symbol}</div>
          )}
        </div>
      ),
    },
    {
      key: 'deployer',
      label: 'Deployer',
      render: (value) => (
        <span className="font-mono text-sm">{formatAddress(value)}</span>
      ),
    },
    {
      key: 'deployedAt',
      label: 'Deployed',
      render: (value) => (
        <span className="text-sm text-primary-400">{formatRelativeTime(value)}</span>
      ),
    },
    ...(showRiskBadge ? [{
      key: 'riskScore',
      label: 'Risk',
      align: 'center',
      render: (value) => (
        <RiskBadge level={value?.level} score={value?.final} size="sm" />
      ),
    }] : []),
    ...(!compact ? [{
      key: 'liquidity',
      label: 'Liquidity',
      render: (_, row) => (
        <span className={row.hasLiquidity ? 'text-success' : 'text-warning'}>
          {row.hasLiquidity ? '✓ Added' : 'No LP'}
        </span>
      ),
    }] : []),
  ];

  return (
    <Table
      columns={columns}
      data={tokens || []}
      onRowClick={(row) => navigate(`/token/${row.address}`)}
      emptyMessage="No tokens found"
    />
  );
};