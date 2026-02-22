import React from 'react';

export const Loading = () => {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="space-y-4 text-center">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-primary-700 rounded-full"></div>
          <div className="absolute top-0 left-0 w-16 h-16 border-4 border-accent rounded-full border-t-transparent animate-spin"></div>
        </div>
        <p className="text-primary-400">Loading intelligence data...</p>
      </div>
    </div>
  );
};