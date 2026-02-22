import React from 'react';

export const Footer = () => {
  return (
    <footer className="border-t border-primary-800 py-4 px-6">
      <div className="flex items-center justify-between text-xs text-primary-500">
        <div className="flex items-center space-x-4">
          <span>© 2024 Sentinel Ledger</span>
          <span>·</span>
          <a href="#" className="hover:text-primary-400 transition-colors">Terms</a>
          <span>·</span>
          <a href="#" className="hover:text-primary-400 transition-colors">Privacy</a>
        </div>
        <div className="flex items-center space-x-4">
          <span>Base Mainnet</span>
          <span>·</span>
          <span>v1.0.0</span>
          <span>·</span>
          <span className="flex items-center">
            <span className="w-2 h-2 bg-success rounded-full animate-pulse mr-2"></span>
            Live
          </span>
        </div>
      </div>
    </footer>
  );
};