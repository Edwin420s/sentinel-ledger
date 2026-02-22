import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { TokenDetail } from './pages/TokenDetail';
import { WalletDetail } from './pages/WalletDetail';
import { Explorer } from './pages/Explorer';
import { RiskFeed } from './pages/RiskFeed';
import { Analytics } from './pages/Analytics';
import { Settings } from './pages/Settings';

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/explorer" element={<Explorer />} />
      <Route path="/token/:address" element={<TokenDetail />} />
      <Route path="/wallet/:address" element={<WalletDetail />} />
      <Route path="/risk-feed" element={<RiskFeed />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  );
};