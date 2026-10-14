import React from 'react';
import { Box, List, ListItemButton, ListItemIcon, ListItemText, Typography } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import PeopleIcon from '@mui/icons-material/People';
import HubIcon from '@mui/icons-material/Hub';
import HttpIcon from '@mui/icons-material/Http';
import PhoneAndroidIcon from '@mui/icons-material/PhoneAndroid';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import ScienceIcon from '@mui/icons-material/Science';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { useNavigate, useLocation } from 'react-router-dom';

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const secOpsItems = [
    { text: 'Overview & Metrics', icon: <DashboardIcon />, path: '/' },
    { text: 'Grafana Observability', icon: <AssessmentIcon sx={{ color: '#F05A28' }} />, path: '/grafana' },
    { text: 'Threat Telemetry', icon: <WarningAmberIcon />, path: '/threats' },
    { text: 'Cross-Layer Correlation', icon: <HubIcon />, path: '/correlation' },
    { text: 'API Gateway Security', icon: <HttpIcon />, path: '/api-security' },
    { text: 'Device Fleet Posture', icon: <PhoneAndroidIcon />, path: '/devices' },
    { text: 'SIEM Audit Logs', icon: <FormatListBulletedIcon />, path: '/audit' },
    { text: 'User Management', icon: <PeopleIcon />, path: '/users' },
  ];

  const researchItems = [
    { text: 'Research Analytics', icon: <ScienceIcon />, path: '/research-analytics' },
    { text: 'Policy & Thresholds', icon: <AdminPanelSettingsIcon />, path: '/policies' },
  ];

  return (
    <Box
      sx={{
        width: 260,
        flexShrink: 0,
        bgcolor: '#0D1424',
        borderRight: '1px solid #1E293B',
        minHeight: 'calc(100vh - 64px)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        p: 2,
      }}
    >
      <Box>
        <Typography variant="overline" sx={{ color: '#64748B', px: 2, letterSpacing: 1.5, fontWeight: 700 }}>
          SECURITY OPERATIONS
        </Typography>
        <List sx={{ mt: 0.5, mb: 2 }}>
          {secOpsItems.map((item) => {
            const isSelected = location.pathname === item.path;
            return (
              <ListItemButton
                key={item.text}
                onClick={() => navigate(item.path)}
                selected={isSelected}
                sx={{
                  borderRadius: 2,
                  mb: 0.6,
                  color: isSelected ? '#00E5FF' : '#94A3B8',
                  bgcolor: isSelected ? 'rgba(0, 229, 255, 0.08) !important' : 'transparent',
                  border: isSelected ? '1px solid rgba(0, 229, 255, 0.3)' : '1px solid transparent',
                  '&:hover': {
                    bgcolor: 'rgba(255, 255, 255, 0.03)',
                  },
                }}
              >
                <ListItemIcon sx={{ color: isSelected ? '#00E5FF' : '#64748B', minWidth: 38 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  primaryTypographyProps={{ fontSize: '0.88rem', fontWeight: isSelected ? 600 : 500 }}
                />
              </ListItemButton>
            );
          })}
        </List>

        <Typography variant="overline" sx={{ color: '#64748B', px: 2, letterSpacing: 1.5, fontWeight: 700 }}>
          RESEARCH & EVALUATION
        </Typography>
        <List sx={{ mt: 0.5 }}>
          {researchItems.map((item) => {
            const isSelected = location.pathname === item.path;
            return (
              <ListItemButton
                key={item.text}
                onClick={() => navigate(item.path)}
                selected={isSelected}
                sx={{
                  borderRadius: 2,
                  mb: 0.6,
                  color: isSelected ? '#00E5FF' : '#94A3B8',
                  bgcolor: isSelected ? 'rgba(0, 229, 255, 0.08) !important' : 'transparent',
                  border: isSelected ? '1px solid rgba(0, 229, 255, 0.3)' : '1px solid transparent',
                  '&:hover': {
                    bgcolor: 'rgba(255, 255, 255, 0.03)',
                  },
                }}
              >
                <ListItemIcon sx={{ color: isSelected ? '#00E5FF' : '#64748B', minWidth: 38 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  primaryTypographyProps={{ fontSize: '0.88rem', fontWeight: isSelected ? 600 : 500 }}
                />
              </ListItemButton>
            );
          })}
        </List>
      </Box>

      <Box sx={{ p: 2, bgcolor: '#111827', borderRadius: 2, border: '1px solid #1E293B', mt: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <HubIcon sx={{ color: '#00E5FF', fontSize: 18 }} />
          <Typography variant="caption" sx={{ fontWeight: 700, color: '#F8FAFC' }}>
            FRAMEWORK TOPOLOGY
          </Typography>
        </Box>
        <Typography variant="caption" sx={{ color: '#64748B', display: 'block', fontSize: 11 }}>
          Gateway: :8080 (Healthy)<br />
          Threat/Correlation: :8084<br />
          Auth: :8081 | User: :8082<br />
          Business: :8083 | Audit: :8085
        </Typography>
      </Box>
    </Box>
  );
};
