import React from 'react';
import clsx from 'clsx';

export const Divider = ({ orientation = 'horizontal', className = '' }) => {
  return (
    <div
      className={clsx(
        'bg-primary-700',
        orientation === 'horizontal' ? 'h-px w-full' : 'w-px h-full',
        className
      )}
    />
  );
};