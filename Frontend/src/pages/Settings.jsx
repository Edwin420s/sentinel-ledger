import React from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { Select } from '../components/common/Select';
import { Divider } from '../components/common/Divider';
import { useSettings } from '../context/SettingsContext';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { Save, RefreshCw, Bell, Shield, Globe, Moon, Sun } from '../assets/icons';
import toast from 'react-hot-toast';

export const Settings = () => {
  const { settings, updateSettings } = useSettings();
  const [theme, setTheme] = useLocalStorage('theme', 'dark');
  const [apiKey, setApiKey] = useLocalStorage('apiKey', '');
  const [formData, setFormData] = React.useState(settings);

  const handleChange = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    updateSettings(formData);
    toast.success('Settings saved successfully');
  };

  const handleReset = () => {
    setFormData(settings);
    toast.success('Settings reset');
  };

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
    toast.success(`${newTheme} theme activated`);
  };

  const refreshOptions = [
    { value: '10000', label: '10 seconds' },
    { value: '30000', label: '30 seconds' },
    { value: '60000', label: '1 minute' },
    { value: '300000', label: '5 minutes' },
  ];

  const riskThresholds = [
    { value: '30', label: 'Low (30)' },
    { value: '50', label: 'Moderate (50)' },
    { value: '70', label: 'High (70)' },
    { value: '85', label: 'Critical (85)' },
  ];

  const views = [
    { value: 'dashboard', label: 'Dashboard' },
    { value: 'explorer', label: 'Explorer' },
    { value: 'risk-feed', label: 'Risk Feed' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Settings</h1>
          <p className="text-primary-400 mt-1">
            Configure your preferences
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" onClick={handleReset} icon={RefreshCw}>
            Reset
          </Button>
          <Button variant="primary" onClick={handleSave} icon={Save}>
            Save Changes
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Navigation */}
        <Card className="lg:col-span-1">
          <nav className="space-y-1">
            <a href="#general" className="block px-4 py-2 bg-primary-700/30 rounded-lg text-accent">
              General
            </a>
            <a href="#notifications" className="block px-4 py-2 hover:bg-primary-700/30 rounded-lg transition-colors">
              Notifications
            </a>
            <a href="#api" className="block px-4 py-2 hover:bg-primary-700/30 rounded-lg transition-colors">
              API & Integrations
            </a>
            <a href="#security" className="block px-4 py-2 hover:bg-primary-700/30 rounded-lg transition-colors">
              Security
            </a>
          </nav>
        </Card>

        {/* Right Column - Settings Forms */}
        <div className="lg:col-span-2 space-y-6">
          {/* General Settings */}
          <Card id="general" title="General Settings">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {theme === 'dark' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
                  <div>
                    <p className="font-medium">Theme</p>
                    <p className="text-sm text-primary-400">Switch between light and dark mode</p>
                  </div>
                </div>
                <Button variant="outline" onClick={toggleTheme}>
                  {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
                </Button>
              </div>

              <Divider />

              <div className="grid grid-cols-2 gap-4">
                <Select
                  label="Default Chain"
                  value={formData.defaultChain || 'base'}
                  onChange={(e) => handleChange('defaultChain', e.target.value)}
                  options={[
                    { value: 'base', label: 'Base' },
                    { value: 'ethereum', label: 'Ethereum' },
                    { value: 'both', label: 'Both' },
                  ]}
                />

                <Select
                  label="Default View"
                  value={formData.defaultView || 'dashboard'}
                  onChange={(e) => handleChange('defaultView', e.target.value)}
                  options={views}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Select
                  label="Refresh Interval"
                  value={formData.refreshInterval || '30000'}
                  onChange={(e) => handleChange('refreshInterval', parseInt(e.target.value))}
                  options={refreshOptions}
                />

                <Select
                  label="Risk Threshold"
                  value={formData.riskThreshold || '50'}
                  onChange={(e) => handleChange('riskThreshold', parseInt(e.target.value))}
                  options={riskThresholds}
                />
              </div>
            </div>
          </Card>

          {/* Notification Settings */}
          <Card id="notifications" title="Notification Settings">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Bell className="w-5 h-5" />
                  <div>
                    <p className="font-medium">Enable Alerts</p>
                    <p className="text-sm text-primary-400">Receive real-time risk alerts</p>
                  </div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={formData.alertsEnabled}
                    onChange={(e) => handleChange('alertsEnabled', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-primary-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent"></div>
                </label>
              </div>

              {formData.alertsEnabled && (
                <>
                  <Divider />
                  <div className="space-y-3">
                    <label className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        className="form-checkbox bg-primary-700 border-primary-600 rounded"
                        checked={formData.alertTypes?.highRisk}
                        onChange={(e) => handleChange('alertTypes', { ...formData.alertTypes, highRisk: e.target.checked })}
                      />
                      <span className="text-sm">High Risk Tokens</span>
                    </label>
                    <label className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        className="form-checkbox bg-primary-700 border-primary-600 rounded"
                        checked={formData.alertTypes?.newDeployments}
                        onChange={(e) => handleChange('alertTypes', { ...formData.alertTypes, newDeployments: e.target.checked })}
                      />
                      <span className="text-sm">New Deployments</span>
                    </label>
                    <label className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        className="form-checkbox bg-primary-700 border-primary-600 rounded"
                        checked={formData.alertTypes?.rugDetected}
                        onChange={(e) => handleChange('alertTypes', { ...formData.alertTypes, rugDetected: e.target.checked })}
                      />
                      <span className="text-sm">Rug Detected</span>
                    </label>
                  </div>
                </>
              )}
            </div>
          </Card>

          {/* API Settings */}
          <Card id="api" title="API & Integrations">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Globe className="w-5 h-5" />
                <div className="flex-1">
                  <p className="font-medium">API Key</p>
                  <p className="text-sm text-primary-400">Used for authenticated requests</p>
                </div>
              </div>
              <Input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your API key"
              />
              <p className="text-xs text-primary-500">
                Your API key is stored locally and never shared
              </p>
            </div>
          </Card>

          {/* Security Settings */}
          <Card id="security" title="Security">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Shield className="w-5 h-5" />
                <div>
                  <p className="font-medium">Data Privacy</p>
                  <p className="text-sm text-primary-400">Manage your data preferences</p>
                </div>
              </div>

              <Divider />

              <div className="space-y-3">
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    className="form-checkbox bg-primary-700 border-primary-600 rounded"
                    defaultChecked
                  />
                  <span className="text-sm">Store search history</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    className="form-checkbox bg-primary-700 border-primary-600 rounded"
                    defaultChecked
                  />
                  <span className="text-sm">Enable analytics tracking</span>
                </label>
              </div>

              <Button variant="outline" size="sm">
                Clear Local Data
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};