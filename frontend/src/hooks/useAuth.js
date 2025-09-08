import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import sessionManager from '../utils/sessionManager';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loginInProgress, setLoginInProgress] = useState(false);
  const navigate = useNavigate();

  // Check if user is authenticated
  const isAuthenticated = !!user && !!localStorage.getItem('access_token');

  // Clear all authentication data
  const clearAuth = useCallback(() => {
    sessionManager.clearSession();
    setUser(null);
    setError(null);
  }, []);

  // Check authentication status
  const checkAuthStatus = useCallback(async () => {
    // Don't check auth if login is in progress
    if (loginInProgress) {
      return;
    }

    const token = localStorage.getItem('access_token');
    
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      setError(null);
      const userData = await authAPI.getProfile();
      
      // Validate session
      if (!sessionManager.isSessionValid(userData.id || userData.username)) {
        console.log('Session validation failed, clearing auth');
        clearAuth();
        setLoading(false);
        return;
      }
      
      setUser(userData);
      // Store user data in localStorage for persistence
      localStorage.setItem('user_data', JSON.stringify(userData));
    } catch (error) {
      console.error('Auth check error:', error);
      clearAuth();
      // Don't redirect here, let the component handle it
    } finally {
      setLoading(false);
    }
  }, [clearAuth, loginInProgress]);

  // Initialize auth state
  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  // Login function
  const login = async (credentials) => {
    try {
      setLoginInProgress(true);
      setLoading(true);
      setError(null);

      // Clear any existing auth data first
      clearAuth();

      // Attempt login
      const data = await authAPI.login(credentials);
      
      // Store tokens
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      
      // Get and store user profile
      try {
        const userData = await authAPI.getProfile();
        
        // Start new session for this user
        sessionManager.startSession(userData.id || userData.username);
        
        setUser(userData);
        localStorage.setItem('user_data', JSON.stringify(userData));
      } catch (profileError) {
        console.error('Failed to get user profile:', profileError);
        // Set basic user info if profile fetch fails
        const basicUser = { username: credentials.username };
        sessionManager.startSession(basicUser.username);
        setUser(basicUser);
        localStorage.setItem('user_data', JSON.stringify(basicUser));
      }
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.non_field_errors?.[0] || 
                          'Login failed. Please check your credentials.';
      setError(errorMessage);
      clearAuth();
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
      setLoginInProgress(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      setLoading(true);
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        // Call backend logout to blacklist token
        await authAPI.logout({ refresh_token: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
      // Continue with local logout even if backend call fails
    } finally {
      // Clear all auth data
      clearAuth();
      setLoading(false);
      // Redirect to login page
      navigate('/login', { replace: true });
    }
  };

  // Refresh token function
  const refreshToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      clearAuth();
      return false;
    }

    try {
      const response = await authAPI.refreshToken({ refresh: refreshToken });
      localStorage.setItem('access_token', response.access);
      if (response.refresh) {
        localStorage.setItem('refresh_token', response.refresh);
      }
      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      clearAuth();
      return false;
    }
  }, [clearAuth]);

  // Force logout (for session conflicts)
  const forceLogout = useCallback(() => {
    clearAuth();
    navigate('/login', { replace: true });
  }, [clearAuth, navigate]);

  // Get session info for debugging
  const getSessionInfo = useCallback(() => {
    return sessionManager.getSessionInfo();
  }, []);

  return {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    refreshToken,
    forceLogout,
    checkAuthStatus,
    clearAuth,
    getSessionInfo
  };
}; 