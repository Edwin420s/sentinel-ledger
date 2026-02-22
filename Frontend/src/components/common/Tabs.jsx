import React, { useState } from 'react';
import clsx from 'clsx';

export const Tabs = ({ tabs, defaultTab, onChange, children }) => {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
    onChange?.(tabId);
  };

  return (
    <div>
      <div className="border-b border-primary-700">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              className={clsx(
                'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === tab.id
                  ? 'border-accent text-accent'
                  : 'border-transparent text-primary-400 hover:text-primary-200 hover:border-primary-600'
              )}
            >
              {tab.label}
              {tab.count !== undefined && (
                <span className="ml-2 px-2 py-0.5 bg-primary-700 rounded-full text-xs">
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>
      <div className="py-4">
        {React.Children.map(children, (child) => {
          if (child.props.tab === activeTab) {
            return child;
          }
          return null;
        })}
      </div>
    </div>
  );
};

export const TabPanel = ({ tab, children }) => {
  return <div>{children}</div>;
};