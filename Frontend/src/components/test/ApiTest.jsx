import React, { useState, useEffect } from 'react';
import { tokenApi } from '../../services/api';

const ApiTest = () => {
  const [status, setStatus] = useState('loading');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      // Test health endpoint
      const healthResponse = await fetch('http://localhost:8000/health');
      const healthData = await healthResponse.json();
      
      if (healthResponse.ok) {
        setStatus('connected');
        setData(healthData);
      } else {
        setStatus('error');
        setError('API health check failed');
      }
    } catch (err) {
      setStatus('error');
      setError(err.message);
    }
  };

  const testTokens = async () => {
    try {
      const tokens = await tokenApi.getTokens({ limit: 5 });
      setData(prev => ({ ...prev, tokens }));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-6 bg-slate-900 rounded-lg border border-slate-700">
      <h2 className="text-xl font-bold text-white mb-4">API Connection Test</h2>
      
      <div className="mb-4">
        <span className="text-gray-400">Status: </span>
        <span className={`font-semibold ${
          status === 'connected' ? 'text-green-400' : 
          status === 'loading' ? 'text-yellow-400' : 'text-red-400'
        }`}>
          {status.toUpperCase()}
        </span>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-300">
          Error: {error}
        </div>
      )}

      {data && (
        <div className="space-y-4">
          <div className="p-3 bg-slate-800 rounded">
            <h3 className="text-white font-semibold mb-2">Health Check:</h3>
            <pre className="text-gray-300 text-sm overflow-auto">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>

          <button
            onClick={testTokens}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
          >
            Test Tokens API
          </button>

          {data.tokens && (
            <div className="p-3 bg-slate-800 rounded">
              <h3 className="text-white font-semibold mb-2">Recent Tokens:</h3>
              <div className="text-gray-300 text-sm">
                Found {data.tokens.length} tokens
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ApiTest;
