import React from 'react';
import clsx from 'clsx';

export const Input = ({
  label,
  error,
  icon: Icon,
  className = '',
  ...props
}) => {
  return (
    <div className="space-y-1">
      {label && (
        <label className="text-sm text-primary-400 font-medium">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2">
            <Icon className="w-4 h-4 text-primary-500" />
          </div>
        )}
        <input
          className={clsx(
            'w-full bg-primary-800/50 border rounded-lg px-4 py-2 text-primary-100',
            'placeholder:text-primary-500 focus:outline-none focus:ring-2 focus:ring-accent/50',
            'transition-all duration-200',
            Icon && 'pl-10',
            error ? 'border-error' : 'border-primary-700',
            className
          )}
          {...props}
        />
      </div>
      {error && (
        <p className="text-xs text-error mt-1">{error}</p>
      )}
    </div>
  );
};