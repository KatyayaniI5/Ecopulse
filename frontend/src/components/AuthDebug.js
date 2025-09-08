import React from 'react';
import { useAuth } from '../hooks/useAuth';

const AuthDebug = () => {
  const { user, isAuthenticated, loading, error, getSessionInfo } = useAuth();
  const sessionInfo = getSessionInfo();

  if (loading) {
    return <div className="p-4 bg-yellow-100 border border-yellow-400 rounded">Loading auth state...</div>;
  }

  return (
    <div className="p-4 bg-gray-100 border border-gray-400 rounded mb-4">
      <h3 className="font-bold text-lg mb-2">Authentication Debug Info</h3>
      
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <strong>Auth Status:</strong> {isAuthenticated ? '✅ Authenticated' : '❌ Not Authenticated'}
        </div>
        <div>
          <strong>User:</strong> {user ? user.username : 'None'}
        </div>
        <div>
          <strong>Session ID:</strong> {sessionInfo.sessionId || 'None'}
        </div>
        <div>
          <strong>User ID:</strong> {sessionInfo.userId || 'None'}
        </div>
        <div>
          <strong>Has Tokens:</strong> {sessionInfo.hasTokens ? '✅ Yes' : '❌ No'}
        </div>
        <div>
          <strong>Has User Data:</strong> {sessionInfo.hasUserData ? '✅ Yes' : '❌ No'}
        </div>
      </div>
      
      {error && (
        <div className="mt-2 p-2 bg-red-100 border border-red-400 rounded text-red-700">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {user && (
        <div className="mt-2 p-2 bg-green-100 border border-green-400 rounded">
          <strong>User Data:</strong>
          <pre className="text-xs mt-1">{JSON.stringify(user, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default AuthDebug; 