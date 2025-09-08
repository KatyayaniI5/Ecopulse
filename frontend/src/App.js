import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import ProtectedRoute from './components/ProtectedRoute';
import PublicRoute from './components/PublicRoute';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import UploadInvoicePage from './pages/UploadInvoicePage';
import CarbonScorePage from './pages/CarbonScorePage';
import AISuggestionsPage from './pages/AISuggestionsPage';
import WhatIfSimulatorPage from './pages/WhatIfSimulatorPage';
import SettingsPage from './pages/SettingsPage';
import LoadingSpinner from './components/LoadingSpinner';
import ApiTest from './components/ApiTest';

function App() {
  const { loading } = useAuth();

  // Show loading spinner while checking authentication
  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="App">
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/api-test" element={<ApiTest />} />
        
        {/* Auth routes - redirect if already authenticated */}
        <Route 
          path="/login" 
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          } 
        />
        <Route 
          path="/register" 
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          } 
        />

        {/* Protected routes - require authentication */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Layout>
                <DashboardPage />
              </Layout>
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/upload" 
          element={
            <ProtectedRoute>
              <Layout>
                <UploadInvoicePage />
              </Layout>
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/carbon-score" 
          element={
            <ProtectedRoute>
              <Layout>
                <CarbonScorePage />
              </Layout>
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/ai-suggestions" 
          element={
            <ProtectedRoute>
              <Layout>
                <AISuggestionsPage />
              </Layout>
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/what-if" 
          element={
            <ProtectedRoute>
              <Layout>
                <WhatIfSimulatorPage />
              </Layout>
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/settings" 
          element={
            <ProtectedRoute>
              <Layout>
                <SettingsPage />
              </Layout>
            </ProtectedRoute>
          } 
        />

        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  );
}

export default App; 