import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { TokenDetail } from './pages/TokenDetail';
import { WalletDetail } from './pages/WalletDetail';
import { Explorer } from './pages/Explorer';
import { RiskFeed } from './pages/RiskFeed';
import { Analytics } from './pages/Analytics';
import { Settings } from './pages/Settings';
import { ErrorBoundary } from './components/common/ErrorBoundary';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/token/:address" element={<TokenDetail />} />
              <Route path="/wallet/:address" element={<WalletDetail />} />
              <Route path="/explorer" element={<Explorer />} />
              <Route path="/risk-feed" element={<RiskFeed />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Layout>
        </Router>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;