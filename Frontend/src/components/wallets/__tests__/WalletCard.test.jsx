import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { WalletCard } from '../WalletCard';
import { describe, it, expect } from 'vitest';

const mockWallet = {
  address: '0x1234567890123456789012345678901234567890',
  stats: {
    erc20Count: 5,
    suspectedRugs: 2,
    firstSeen: '2024-01-01T00:00:00Z',
  },
  chains: ['base', 'ethereum'],
  riskScore: 65,
};

describe('WalletCard', () => {
  it('renders wallet address correctly', () => {
    render(
      <BrowserRouter>
        <WalletCard wallet={mockWallet} />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/0x1234...7890/)).toBeInTheDocument();
  });

  it('displays token count', () => {
    render(
      <BrowserRouter>
        <WalletCard wallet={mockWallet} />
      </BrowserRouter>
    );
    
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('shows suspected rugs', () => {
    render(
      <BrowserRouter>
        <WalletCard wallet={mockWallet} />
      </BrowserRouter>
    );
    
    expect(screen.getByText('2')).toBeInTheDocument();
  });
});