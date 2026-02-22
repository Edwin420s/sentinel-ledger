import React from 'react';
import { Card } from '../common/Card';
import { Tooltip } from '../common/Tooltip';
import { formatCurrency } from '../../services/utils/formatters';

export const LiquidityMetrics = ({ pools }) => {
  const totalInitialLiquidity = pools?.reduce((sum, pool) => 
    sum + (pool.initialLiquidityUsd || 0), 0
  ) || 0;

  const totalCurrentLiquidity = pools?.reduce((sum, pool) => 
    sum + (pool.currentLiquidityUsd || 0), 0
  ) || 0;

  const lockedPools = pools?.filter(p => p.liquidityLocked).length || 0;
  const unlockedPools = (pools?.length || 0) - lockedPools;

  const liquidityChange = totalInitialLiquidity ? 
    ((totalCurrentLiquidity - totalInitialLiquidity) / totalInitialLiquidity * 100).toFixed(1) : 0;

  return (
    <Card title="Liquidity Overview">
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-primary-400 text-sm">Total Initial</p>
            <p className="text-xl font-semibold mt-1">{formatCurrency(totalInitialLiquidity)}</p>
          </div>
          <div>
            <p className="text-primary-400 text-sm">Current</p>
            <p className="text-xl font-semibold mt-1">{formatCurrency(totalCurrentLiquidity)}</p>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-primary-400 text-sm">Change</span>
          <span className={liquidityChange >= 0 ? 'text-success' : 'text-error'}>
            {liquidityChange}%
          </span>
        </div>

        <div className="pt-4 border-t border-primary-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Tooltip content="Pools with locked liquidity">
                <span className="text-primary-400 text-sm">Locked</span>
              </Tooltip>
            </div>
            <span className="font-medium">{lockedPools}</span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <div className="flex items-center space-x-2">
              <Tooltip content="Pools with unlocked liquidity">
                <span className="text-primary-400 text-sm">Unlocked</span>
              </Tooltip>
            </div>
            <span className="font-medium text-warning">{unlockedPools}</span>
          </div>
        </div>
      </div>
    </Card>
  );
};