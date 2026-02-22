import React from 'react';
import clsx from 'clsx';

const riskStyles = {
  LOW: 'risk-low',
  MODERATE: 'risk-moderate',
  HIGH: 'risk-high',
  CRITICAL: 'risk-critical',
};

export const RiskBadge = ({ level, score, size = 'md' }) => {
  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base',
  };

  return (
    <div className={clsx(
      'inline-flex items-center space-x-2 rounded-full font-medium',
      riskStyles[level],
      sizeStyles[size]
    )}>
      <span className="capitalize">{level.toLowerCase()}</span>
      {score !== undefined && (
        <>
          <span className="text-primary-400">·</span>
          <span className="font-mono">{score}</span>
        </>
      )}
    </div>
  );
};