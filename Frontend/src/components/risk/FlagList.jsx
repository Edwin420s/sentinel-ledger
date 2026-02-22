import React from 'react';
import { AlertTriangle, Info, ShieldAlert } from '../../assets/icons';
import { Card } from '../common/Card';
import clsx from 'clsx';

const severityIcons = {
  info: Info,
  warning: AlertTriangle,
  critical: ShieldAlert,
};

const severityStyles = {
  info: 'border-info/20 bg-info/5 text-info',
  warning: 'border-warning/20 bg-warning/5 text-warning',
  critical: 'border-error/20 bg-error/5 text-error',
};

export const FlagList = ({ flags, title = 'Risk Flags' }) => {
  if (!flags?.length) {
    return (
      <Card title={title}>
        <div className="py-8 text-center text-primary-500">
          No risk flags detected
        </div>
      </Card>
    );
  }

  return (
    <Card title={title}>
      <div className="space-y-3">
        {flags.map((flag, index) => {
          const Icon = severityIcons[flag.severity];
          
          return (
            <div
              key={index}
              className={clsx(
                'p-3 rounded-lg border',
                severityStyles[flag.severity]
              )}
            >
              <div className="flex items-start space-x-3">
                <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm">{flag.description}</p>
                  <div className="flex items-center space-x-3 mt-2">
                    <span className="text-xs opacity-75 capitalize">
                      {flag.category}
                    </span>
                    <span className="text-xs opacity-75">
                      Weight: {flag.weight}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};