import React from 'react';
import { Card } from '../common/Card';
import { Tooltip } from '../common/Tooltip';
import { RiskBadge } from './RiskBadge';
import clsx from 'clsx';

const categories = [
  { key: 'contract', label: 'Contract Risk', weight: 35 },
  { key: 'liquidity', label: 'Liquidity Risk', weight: 30 },
  { key: 'ownership', label: 'Ownership Risk', weight: 20 },
  { key: 'deployer', label: 'Deployer History', weight: 15 },
];

const getScoreColor = (score) => {
  if (score < 30) return 'text-risk-low';
  if (score < 60) return 'text-risk-moderate';
  if (score < 80) return 'text-risk-high';
  return 'text-risk-critical';
};

export const ScoreBreakdown = ({ scores }) => {
  return (
    <Card title="Risk Score Breakdown">
      <div className="space-y-4">
        {categories.map(({ key, label, weight }) => {
          const score = scores[key];
          
          return (
            <div key={key}>
              <div className="flex justify-between text-sm mb-1">
                <div className="flex items-center space-x-2">
                  <span className="text-primary-300">{label}</span>
                  <Tooltip content={`Weight: ${weight}% of final score`}>
                    <span className="text-primary-500 cursor-help">ⓘ</span>
                  </Tooltip>
                </div>
                <span className={clsx('font-mono font-medium', getScoreColor(score))}>
                  {score}/100
                </span>
              </div>
              <div className="h-2 bg-primary-700 rounded-full overflow-hidden">
                <div
                  className={clsx(
                    'h-full rounded-full transition-all',
                    score < 30 ? 'bg-risk-low' :
                    score < 60 ? 'bg-risk-moderate' :
                    score < 80 ? 'bg-risk-high' : 'bg-risk-critical'
                  )}
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>
          );
        })}

        <div className="pt-4 mt-4 border-t border-primary-700">
          <div className="flex justify-between items-center">
            <span className="text-primary-300 font-medium">Final Risk Score</span>
            <div className="flex items-center space-x-3">
              <span className={clsx(
                'text-2xl font-bold font-mono',
                getScoreColor(scores.final)
              )}>
                {scores.final}
              </span>
              <RiskBadge level={scores.level} />
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};