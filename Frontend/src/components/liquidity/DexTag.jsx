import React from 'react';

const dexConfig = {
  uniswap: {
    name: 'Uniswap',
    bg: 'bg-blue-500/10',
    text: 'text-blue-400',
    border: 'border-blue-500/20',
  },
  aerodrome: {
    name: 'Aerodrome',
    bg: 'bg-purple-500/10',
    text: 'text-purple-400',
    border: 'border-purple-500/20',
  },
  other: {
    name: 'Other DEX',
    bg: 'bg-primary-700',
    text: 'text-primary-300',
    border: 'border-primary-600',
  },
};

export const DexTag = ({ dex }) => {
  const config = dexConfig[dex] || dexConfig.other;

  return (
    <span className={`px-2 py-1 text-xs rounded-full border ${config.bg} ${config.text} ${config.border}`}>
      {config.name}
    </span>
  );
};