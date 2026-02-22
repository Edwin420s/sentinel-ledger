import React, { createContext, useState, useEffect } from 'react';

export const SettingsContext = createContext();

const defaultSettings = {
  defaultChain: 'base',
  refreshInterval: 30000,
  alertsEnabled: true,
  riskThreshold: 50,
  defaultView: 'dashboard',
  alertTypes: {
    highRisk: true,
    newDeployments: true,
    rugDetected: true,
    liquidityChange: false,
  },
  theme: 'dark',
  compactMode: false,
  showTestnets: false,
  language: 'en',
};

export const SettingsProvider = ({ children }) => {
  const [settings, setSettings] = useState(() => {
    const saved = localStorage.getItem('settings');
    return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
  });

  useEffect(() => {
    localStorage.setItem('settings', JSON.stringify(settings));
  }, [settings]);

  const updateSettings = (newSettings) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  const resetSettings = () => {
    setSettings(defaultSettings);
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSettings, resetSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};