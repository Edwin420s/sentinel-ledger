import React from 'react';
import { AlertCircle, AlertTriangle, Info, CheckCircle, X } from '../../assets/icons';
import clsx from 'clsx';

const variants = {
  info: {
    bg: 'bg-info/10',
    border: 'border-info/20',
    text: 'text-info',
    icon: Info,
  },
  success: {
    bg: 'bg-success/10',
    border: 'border-success/20',
    text: 'text-success',
    icon: CheckCircle,
  },
  warning: {
    bg: 'bg-warning/10',
    border: 'border-warning/20',
    text: 'text-warning',
    icon: AlertTriangle,
  },
  error: {
    bg: 'bg-error/10',
    border: 'border-error/20',
    text: 'text-error',
    icon: AlertCircle,
  },
};

export const Alert = ({
  variant = 'info',
  title,
  children,
  dismissible = false,
  onDismiss,
  className = '',
}) => {
  const Icon = variants[variant].icon;

  return (
    <div
      className={clsx(
        'rounded-lg border p-4',
        variants[variant].bg,
        variants[variant].border,
        className
      )}
    >
      <div className="flex">
        <div className="flex-shrink-0">
          <Icon className={clsx('w-5 h-5', variants[variant].text)} />
        </div>
        <div className="ml-3 flex-1">
          {title && (
            <h3 className={clsx('text-sm font-medium', variants[variant].text)}>
              {title}
            </h3>
          )}
          {children && (
            <div className={clsx('text-sm', variants[variant].text, title && 'mt-2')}>
              {children}
            </div>
          )}
        </div>
        {dismissible && (
          <button
            onClick={onDismiss}
            className={clsx(
              'ml-auto pl-3',
              variants[variant].text,
              'hover:opacity-75 transition-opacity'
            )}
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
};