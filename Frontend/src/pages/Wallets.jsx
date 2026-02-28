import React, { useState } from 'react';
import { Card } from '../components/common/Card';
import { Loading } from '../components/common/Loading';
import { WalletCard } from '../components/wallets/WalletCard';
import { WalletSearch } from '../components/wallets/WalletSearch';

export const Wallets = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Wallet Explorer</h1>
        <p className="text-primary-400 mt-1">
          Search and analyze wallet addresses on Base
        </p>
      </div>

      <Card>
        <div className="space-y-6">
          <WalletSearch 
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search by wallet address..."
          />
          
          <div className="text-center py-8">
            <p className="text-primary-400">
              Enter a wallet address to view detailed analytics and risk profile
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};
