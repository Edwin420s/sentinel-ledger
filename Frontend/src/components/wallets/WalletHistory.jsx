import React from 'react';
import { Card } from '../common/Card';
import { Table } from '../common/Table';
import { Badge } from '../common/Badge';
import { formatAddress, formatRelativeTime, formatNumber } from '../../services/utils/formatters';
import { ExternalLink } from '../../assets/icons';

export const WalletHistory = ({ transactions }) => {
  const columns = [
    {
      key: 'hash',
      label: 'Transaction',
      render: (value) => (
        <span className="font-mono text-sm">{formatAddress(value)}</span>
      ),
    },
    {
      key: 'type',
      label: 'Type',
      render: (value) => (
        <Badge size="sm" variant={value === 'DEPLOY' ? 'accent' : 'info'}>
          {value}
        </Badge>
      ),
    },
    {
      key: 'timestamp',
      label: 'Time',
      render: (value) => formatRelativeTime(value),
    },
    {
      key: 'value',
      label: 'Value',
      render: (value) => value ? formatNumber(value) : '-',
    },
    {
      key: 'hash',
      label: '',
      render: (value) => (
        <a
          href={`https://basescan.org/tx/${value}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary-500 hover:text-primary-400"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      ),
    },
  ];

  return (
    <Card title="Transaction History">
      <Table
        columns={columns}
        data={transactions || []}
        emptyMessage="No transactions found"
      />
    </Card>
  );
};