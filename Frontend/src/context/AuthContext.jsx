import React, { createContext, useState, useEffect } from 'react';
import { api } from '../services/api/client';
import toast from 'react-hot-toast';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [apiKey, setApiKey] = useState(() => {
    return localStorage.getItem('apiKey') || '';
  });

  useEffect(() => {
    // Validate API key on mount
    if (apiKey) {
      validateApiKey(apiKey);
    } else {
      setLoading(false);
    }
  }, []);

  const validateApiKey = async (key) => {
    try {
      const response = await api.validateApiKey(key);
      setUser(response.user);
    } catch (error) {
      console.error('Invalid API key:', error);
      localStorage.removeItem('apiKey');
      setApiKey('');
    } finally {
      setLoading(false);
    }
  };

  const login = async (key) => {
    try {
      setLoading(true);
      const response = await api.validateApiKey(key);
      localStorage.setItem('apiKey', key);
      setApiKey(key);
      setUser(response.user);
      toast.success('Successfully authenticated');
      return true;
    } catch (error) {
      toast.error('Invalid API key');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('apiKey');
    setApiKey('');
    setUser(null);
    toast.success('Logged out successfully');
  };

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      apiKey,
      login,
      logout,
      isAuthenticated: !!user,
    }}>
      {children}
    </AuthContext.Provider>
  );
};