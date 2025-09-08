import React, { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const ApiTest = () => {
  const [status, setStatus] = useState('Testing...');
  const [error, setError] = useState(null);
  const [backendInfo, setBackendInfo] = useState(null);
  const [loginTest, setLoginTest] = useState(null);

  useEffect(() => {
    testBackendConnection();
  }, []);

  const testBackendConnection = async () => {
    try {
      setStatus('Connecting to backend...');
      
      // Test the root endpoint
      const response = await fetch('http://localhost:8000/');
      if (response.ok) {
        const data = await response.text();
        setBackendInfo(data);
        setStatus('✅ Backend connection successful!');
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (err) {
      setError(err.message);
      setStatus('❌ Backend connection failed');
    }
  };

  const testAuthEndpoint = async () => {
    try {
      setStatus('Testing auth endpoint...');
      const response = await fetch('http://localhost:8000/api/auth/');
      if (response.ok) {
        setStatus('✅ Auth endpoint accessible!');
      } else {
        throw new Error(`Auth endpoint returned ${response.status}`);
      }
    } catch (err) {
      setError(err.message);
      setStatus('❌ Auth endpoint test failed');
    }
  };

  const testLogin = async () => {
    try {
      setStatus('Testing login with your credentials...');
      
      // Test login with the superuser credentials
      const response = await fetch('http://localhost:8000/api/auth/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: 'lokesh_04',
          password: 'your_password_here' // You'll need to replace this with your actual password
        })
      });

      if (response.ok) {
        const data = await response.json();
        setLoginTest('✅ Login successful! Token received.');
        console.log('Login response:', data);
      } else {
        const errorData = await response.json();
        setLoginTest(`❌ Login failed: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setLoginTest(`❌ Login error: ${err.message}`);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Frontend-Backend Connection Test</h2>
      
      <div className="space-y-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-800 mb-2">Connection Status</h3>
          <p className="text-blue-700">{status}</p>
          {error && (
            <p className="text-red-600 mt-2">Error: {error}</p>
          )}
        </div>

        {backendInfo && (
          <div className="p-4 bg-green-50 rounded-lg">
            <h3 className="font-semibold text-green-800 mb-2">Backend Response</h3>
            <pre className="text-sm text-green-700 whitespace-pre-wrap">{backendInfo}</pre>
          </div>
        )}

        {loginTest && (
          <div className="p-4 bg-purple-50 rounded-lg">
            <h3 className="font-semibold text-purple-800 mb-2">Login Test</h3>
            <p className="text-purple-700">{loginTest}</p>
          </div>
        )}

        <div className="flex space-x-4">
          <button
            onClick={testBackendConnection}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Test Connection
          </button>
          <button
            onClick={testAuthEndpoint}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
          >
            Test Auth API
          </button>
          <button
            onClick={testLogin}
            className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
          >
            Test Login
          </button>
        </div>

        <div className="p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-2">Available Endpoints</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <code>/admin/</code> - Django admin</li>
            <li>• <code>/api/auth/token/</code> - JWT login (POST)</li>
            <li>• <code>/api/auth/register/</code> - User registration</li>
            <li>• <code>/api/auth/profile/</code> - User profile</li>
            <li>• <code>/api/invoices/</code> - Invoice management</li>
            <li>• <code>/api/analytics/</code> - Analytics data</li>
            <li>• <code>/api/recommendations/</code> - Recommendations</li>
            <li>• <code>/api/simulations/</code> - Simulations</li>
          </ul>
        </div>

        <div className="p-4 bg-yellow-50 rounded-lg">
          <h3 className="font-semibold text-yellow-800 mb-2">Troubleshooting</h3>
          <ul className="text-sm text-yellow-700 space-y-1">
            <li>• Make sure both backend (port 8000) and frontend (port 3000) are running</li>
            <li>• Check browser console for CORS errors</li>
            <li>• Verify your superuser credentials: <code>lokesh_04</code></li>
            <li>• Test the login endpoint manually with your actual password</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ApiTest;