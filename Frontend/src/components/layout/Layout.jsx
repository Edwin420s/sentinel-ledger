import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { Footer } from './Footer';
import { MobileNav } from './MobileNav';
import { Toaster } from 'react-hot-toast';

export const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-primary-900 text-primary-100">
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#1e293b',
            color: '#f1f5f9',
            border: '1px solid #334155',
          },
        }}
      />
      
      <div className="flex h-screen">
        {/* Desktop Sidebar */}
        <div className="hidden lg:block w-64 flex-shrink-0">
          <Sidebar />
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-w-0">
          <Header />
          
          <main className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="max-w-7xl mx-auto">
              {children}
            </div>
          </main>

          <Footer />
        </div>
      </div>

      {/* Mobile Navigation */}
      <MobileNav />
    </div>
  );
};