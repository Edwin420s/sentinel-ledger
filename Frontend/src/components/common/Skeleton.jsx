import React from 'react';
import clsx from 'clsx';

export const Skeleton = ({ className, variant = 'text', count = 1 }) => {
  const variants = {
    text: 'h-4 rounded',
    circle: 'rounded-full',
    rectangular: 'rounded-lg',
  };

  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={clsx(
            'skeleton',
            variants[variant],
            className
          )}
        />
      ))}
    </>
  );
};

export const TokenCardSkeleton = () => {
  return (
    <div className="card p-6 space-y-4">
      <div className="flex justify-between">
        <Skeleton className="w-32 h-6" />
        <Skeleton className="w-20 h-6" />
      </div>
      <div className="space-y-2">
        <Skeleton className="w-40 h-4" />
        <Skeleton className="w-24 h-4" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <Skeleton className="w-full h-10" />
        <Skeleton className="w-full h-10" />
      </div>
    </div>
  );
};

export const TableRowSkeleton = ({ columns = 4 }) => {
  return (
    <tr>
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="py-3 px-4">
          <Skeleton className="w-full h-4" />
        </td>
      ))}
    </tr>
  );
};