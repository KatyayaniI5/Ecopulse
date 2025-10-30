import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [localError, setLocalError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { login, error: authError, loading: authLoading, isAuthenticated } = useAuth();

  // Get the intended destination from location state
  const from = location.state?.from?.pathname || '/dashboard';

  // Check for success message from registration
  useEffect(() => {
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the message from location state
      navigate(location.pathname, { replace: true });
    }
  }, [location.state, navigate, location.pathname]);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated && !loading && !submitted) {
      console.log('User already authenticated, redirecting to:', from);
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, loading, submitted, navigate, from]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Prevent double submission
    if (loading || submitted) {
      return;
    }

    setLoading(true);
    setSubmitted(true);
    setLocalError('');
    setSuccessMessage('');

    console.log('Login form submitted with:', { username: formData.username });

    try {
      const result = await login({
        username: formData.username,
        password: formData.password
      });

      console.log('Login result:', result);

      if (result.success) {
        console.log('Login successful, redirecting to:', from);
        // Redirect to intended page or dashboard
        navigate(from, { replace: true });
      } else {
        console.log('Login failed:', result.error);
        setLocalError(result.error || 'Login failed. Please try again.');
        setSubmitted(false); // Allow retry
      }
    } catch (err) {
      console.error('Login error:', err);
      setLocalError(err.message || 'An unexpected error occurred. Please try again.');
      setSubmitted(false); // Allow retry
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear error when user starts typing
    if (localError || authError) {
      setLocalError('');
    }
  };

  // Show loading state
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // Combine local and auth errors
  const displayError = localError || authError;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          {from !== '/dashboard' && (
            <p className="mt-2 text-center text-sm text-gray-600">
              Please sign in to access {from}
            </p>
          )}
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {successMessage && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM5.707 9.293a1 1 0 000 1.414l4 4a1 1 0 001.414 0l8-8a1 1 0 00-1.414-1.414L9 12.586l-3.293-3.293a1 1 0 00-1.414 1.414z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium">{successMessage}</p>
                </div>
              </div>
            </div>
          )}
          
          {displayError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium">{displayError}</p>
                </div>
              </div>
            </div>
          )}
          
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                name="username"
                type="text"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                disabled={loading}
                autoComplete="username"
              />
            </div>
            <div>
              <input
                name="password"
                type="password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                disabled={loading}
                autoComplete="current-password"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading || submitted}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Signing in...
                </>
              ) : (
                'Sign in'
              )}
            </button>
          </div>

          <div className="text-center">
            <Link to="/register" className="text-indigo-600 hover:text-indigo-500">
              Don't have an account? Sign up
            </Link>
          </div>
        </form>

        {/* Debug info - remove in production */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mt-4 p-3 bg-gray-100 rounded text-xs">
            <p><strong>Debug Info:</strong></p>
            <p>Username: {formData.username}</p>
            <p>Loading: {loading ? 'Yes' : 'No'}</p>
            <p>Submitted: {submitted ? 'Yes' : 'No'}</p>
            <p>Auth Loading: {authLoading ? 'Yes' : 'No'}</p>
            <p>Is Authenticated: {isAuthenticated ? 'Yes' : 'No'}</p>
            <p>Error: {displayError || 'None'}</p>
            <p>Success Message: {successMessage || 'None'}</p>
            <p>Redirect To: {from}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default LoginPage;