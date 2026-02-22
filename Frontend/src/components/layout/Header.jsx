import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../../context/ThemeContext';
import { useSettings } from '../../context/SettingsContext';
import { Search, Bell, Settings as SettingsIcon, User } from '../../assets/icons';
import { Button } from '../common/Button';
import { Input } from '../common/Input';

export const Header = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { settings } = useSettings();
  const [searchQuery, setSearchQuery] = React.useState('');
  const [showNotifications, setShowNotifications] = React.useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/explorer?search=${searchQuery}`);
    }
  };

  return (
    <header className="bg-primary-800/30 backdrop-blur-sm border-b border-primary-700 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex-1 max-w-xl">
          <Input
            placeholder="Search by token address or deployer..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            icon={Search}
            className="bg-primary-800/50"
          />
        </form>

        {/* Right Section */}
        <div className="flex items-center space-x-3">
          {/* Notifications */}
          <div className="relative">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-error rounded-full"></span>
            </Button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-primary-800 rounded-lg border border-primary-700 shadow-xl z-50">
                <div className="p-3 border-b border-primary-700">
                  <h4 className="font-medium">Notifications</h4>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  <div className="p-4 text-center text-primary-500 text-sm">
                    No new notifications
                  </div>
                </div>
                <div className="p-2 border-t border-primary-700">
                  <Button variant="ghost" size="sm" className="w-full">
                    Mark all as read
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Settings */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/settings')}
            icon={SettingsIcon}
          />

          {/* User Menu */}
          <Button
            variant="ghost"
            size="sm"
            className="flex items-center space-x-2"
          >
            <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center">
              <User className="w-4 h-4 text-accent" />
            </div>
            <span className="text-sm hidden lg:inline">Guest User</span>
          </Button>
        </div>
      </div>
    </header>
  );
};