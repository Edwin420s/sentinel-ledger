import React from 'react';
import { Card } from '../common/Card';
import { DexTag } from './DexTag';
import { formatCurrency, formatAddress } from '../../services/utils/formatters';
import { ExternalLink } from '../../assets/icons';

export const LiquidityCard = ({ pools }) => {
  if (!pools?.length) {
    return (
      <Card title="Liquidity Pools">
        <div className="py-8 text-center text-primary-500">
          No liquidity pools detected
        </div>
      </Card>
    );
  }

  return (
    <Card title="Liquidity Pools">
      <div className="space-y-4">
        {pools.map((pool, index) => (
          <div key={index} className="p-4 bg-primary-700/30 rounded-lg">
            <div className="flex items-center justify-between mb-3">
              <DexTag dex={pool.dex} />
              <span className={pool.liquidityLocked ? 'text-success' : 'text-warning'}>
                {pool.liquidityLocked ? 'Locked' : 'Unlocked'}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <p className="text-primary-400">Initial Liquidity</p>
                <p className="font-medium mt-1">{formatCurrency(pool.initialLiquidityUsd)}</p>
              </div>
              <div>
                <p className="text-primary-400">Current</p>
                <p className="font-medium mt-1">{formatCurrency(pool.currentLiquidityUsd)}</p>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-primary-700">
              <p className="text-xs text-primary-400 mb-1">LP Holder</p>
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm">{formatAddress(pool.lpHolder)}</span>
                <a
                  href={`https://basescan.org/address/${pool.poolAddress}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-accent hover:text-accent-light"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};