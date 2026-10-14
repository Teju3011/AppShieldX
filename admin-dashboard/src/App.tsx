import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { darkTheme } from './theme/theme';
import { AuthProvider, useAuth } from './context/AuthContext';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { DashboardPage } from './pages/DashboardPage';
import { ThreatTelemetryPage } from './pages/ThreatTelemetryPage';
import { CorrelationPage } from './pages/CorrelationPage';
import { ApiSecurityPage } from './pages/ApiSecurityPage';
import { DeviceSecurityPage } from './pages/DeviceSecurityPage';
import { AuditLogsPage } from './pages/AuditLogsPage';
import { UserManagementPage } from './pages/UserManagementPage';
import { PolicyManagementPage } from './pages/PolicyManagementPage';
import { ResearchAnalyticsPage } from './pages/ResearchAnalyticsPage';
import { GrafanaObservabilityPage } from './pages/GrafanaObservabilityPage';
import { LoginPage } from './pages/LoginPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<DashboardPage />} />
              <Route path="grafana" element={<GrafanaObservabilityPage />} />
              <Route path="threats" element={<ThreatTelemetryPage />} />
              <Route path="correlation" element={<CorrelationPage />} />
              <Route path="api-security" element={<ApiSecurityPage />} />
              <Route path="devices" element={<DeviceSecurityPage />} />
              <Route path="audit" element={<AuditLogsPage />} />
              <Route path="users" element={<UserManagementPage />} />
              <Route path="policies" element={<PolicyManagementPage />} />
              <Route path="research-analytics" element={<ResearchAnalyticsPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
