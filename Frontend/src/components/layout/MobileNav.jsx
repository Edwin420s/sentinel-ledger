import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Activity, Shield, Wallet, Settings } from '../../assets/icons';

const navItems = [
  { path: '/', icon: Home, label: 'Home' },
  { path: '/explorer', icon: Activity, label: 'Explore' },
  { path: '/risk-feed', icon: Shield, label: 'Risk' },
  { path: '/wallets', icon: Wallet, label: 'Wallets' },
  { path: '/settings', icon: Settings, label: 'Settings' },
];

export const MobileNav = () => {
  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-primary-800/90 backdrop-blur-md border-t border-primary-700 z-50">
      <div className="flex items-center justify-around py-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex flex-col items-center p-2 rounded-lg transition-colors ${
                isActive ? 'text-accent' : 'text-primary-400 hover:text-primary-200'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="text-xs mt-1">{item.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
};