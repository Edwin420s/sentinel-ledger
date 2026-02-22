import React from 'react';
import { RISK_COLORS, RISK_LEVELS } from '../../services/utils/constants';
import { Tooltip } from '../common/Tooltip';

export const RiskLevelIndicator = ({ level, score, size = 'md', showTooltip = true }) => {
  const getColor = () => {
    switch (level) {
      case RISK_LEVELS.LOW:
        return RISK_COLORS.LOW;
      case RISK_LEVELS.MODERATE:
        return RISK_COLORS.MODERATE;
      case RISK_LEVELS.HIGH:
        return RISK_COLORS.HIGH;
      case RISK_LEVELS.CRITICAL:
        return RISK_COLORS.CRITICAL;
      default:
        return '#94a3b8';
    }
  };

  const sizes = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  const indicator = (
    <div
      className={`${sizes[size]} rounded-full animate-pulse`}
      style={{ backgroundColor: getColor() }}
    />
  );

  if (showTooltip) {
    return (
      <Tooltip content={`${level} Risk${score ? ` (${score})` : ''}`}>
        {indicator}
      </Tooltip>
    );
  }

  return indicator;
};