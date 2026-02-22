import React from 'react';
import { ChevronDown } from '../../assets/icons';
import clsx from 'clsx';

export const Select = ({
  label,
  options = [],
  value,
  onChange,
  error,
  className = '',
  placeholder = 'Select an option',
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
        <select
          className={clsx(
            'w-full bg-primary-800/50 border rounded-lg px-4 py-2 text-primary-100 appearance-none',
            'focus:outline-none focus:ring-2 focus:ring-accent/50',
            'transition-all duration-200',
            error ? 'border-error' : 'border-primary-700',
            className
          )}
          value={value}
          onChange={onChange}
          {...props}
        >
          <option value="" disabled>
            {placeholder}
          </option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-primary-500 pointer-events-none" />
      </div>
      {error && (
        <p className="text-xs text-error mt-1">{error}</p>
      )}
    </div>
  );
};