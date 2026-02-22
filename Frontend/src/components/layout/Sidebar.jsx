import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Shield, 
  Activity, 
  Wallet, 
  LineChart, 
  Settings, 
  Home 
} from '../../assets/icons';

const navItems = [
  {
    path: '/',
    label: 'Dashboard',
    icon: <Home className="w-5 h-5" />,
  },
  {
    path: '/explorer',
    label: 'Explorer',
    icon: <Activity className="w-5 h-5" />,
  },
  {
    path: '/risk-feed',
    label: 'Risk Feed',
    icon: <Shield className="w-5 h-5" />,
  },
  {
    path: '/analytics',
    label: 'Analytics',
    icon: <LineChart className="w-5 h-5" />,
  },
  {
    path: '/wallets',
    label: 'Wallets',
    icon: <Wallet className="w-5 h-5" />,
  },
  {
    path: '/settings',
    label: 'Settings',
    icon: <Settings className="w-5 h-5" />,
  },
];

export const Sidebar = () => {
  return (
    <div className="h-full bg-primary-800/50 backdrop-blur-sm border-r border-primary-700">
      <div className="p-6">
        <div className="flex items-center space-x-2">
          <Shield className="w-8 h-8 text-accent" />
          <span className="text-xl font-semibold tracking-tight">
            Sentinel<span className="text-accent">Ledger</span>
          </span>
        </div>
      </div>

      <nav className="px-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-accent/10 text-accent'
                  : 'text-primary-300 hover:bg-primary-700/50'
              }`
            }
          >
            {item.icon}
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4">
        <div className="px-4 py-3 bg-primary-700/30 rounded-lg">
          <p className="text-xs text-primary-400">
            Base Mainnet
          </p>
          <p className="text-xs text-primary-500 mt-1">
            Last indexed: 2 min ago
          </p>
        </div>
      </div>
    </div>
  );
};