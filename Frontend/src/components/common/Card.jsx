import React from 'react';
import clsx from 'clsx';

export const Card = ({ 
  children, 
  title, 
  subtitle, 
  className = '',
  titleClassName = '',
  ...props 
}) => {
  return (
    <div className={clsx('card p-6', className)} {...props}>
      {(title || subtitle) && (
        <div className="mb-4">
          {title && (
            <h3 className={clsx('text-lg font-medium', titleClassName)}>
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="text-sm text-primary-400 mt-1">{subtitle}</p>
          )}
        </div>
      )}
      {children}
    </div>
  );
};