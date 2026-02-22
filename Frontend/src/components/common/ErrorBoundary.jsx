import React from 'react';
import { AlertCircle } from '../../assets/icons';
import { Button } from './Button';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-primary-900 flex items-center justify-center p-4">
          <div className="text-center max-w-md">
            <div className="inline-flex p-3 bg-error/10 rounded-full mb-4">
              <AlertCircle className="w-8 h-8 text-error" />
            </div>
            <h2 className="text-xl font-semibold mb-2">Something went wrong</h2>
            <p className="text-primary-400 mb-6">
              An error occurred while rendering this page. Please try refreshing.
            </p>
            <Button
              onClick={() => window.location.reload()}
              variant="primary"
            >
              Refresh Page
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}