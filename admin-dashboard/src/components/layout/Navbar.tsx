import React from 'react';
import { AppBar, Toolbar, Typography, Box, Chip, IconButton, Button } from '@mui/material';
import ShieldIcon from '@mui/icons-material/Shield';
import LogoutIcon from '@mui/icons-material/Logout';
import SecurityIcon from '@mui/icons-material/Security';
import { useAuth } from '../../context/AuthContext';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <AppBar position="sticky" elevation={0} sx={{ borderBottom: '1px solid #1E293B', bgcolor: '#0D1424' }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <ShieldIcon sx={{ color: '#00E5FF', fontSize: 30 }} />
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: -0.5, color: '#F8FAFC', lineHeight: 1.2 }}>
              APPSHIELD<span style={{ color: '#00E5FF' }}>X</span>
            </Typography>
            <Typography variant="caption" sx={{ color: '#64748B', fontFamily: "'JetBrains Mono', monospace" }}>
              Runtime Protection & API Security Console
            </Typography>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip
            icon={<SecurityIcon sx={{ color: '#10B981 !important', fontSize: 16 }} />}
            label="ZERO-TRUST ACTIVE"
            size="small"
            sx={{
              bgcolor: 'rgba(16, 185, 129, 0.1)',
              color: '#10B981',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              fontFamily: "'JetBrains Mono', monospace",
            }}
          />

          {user && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="body2" sx={{ color: '#94A3B8' }}>
                {user.email}
              </Typography>
              <Chip
                label={user.roles?.includes('ROLE_ADMIN') ? 'ADMIN' : 'USER'}
                size="small"
                color={user.roles?.includes('ROLE_ADMIN') ? 'primary' : 'default'}
                sx={{ fontSize: 10, height: 20 }}
              />
            </Box>
          )}

          <Button
            variant="outlined"
            color="error"
            size="small"
            startIcon={<LogoutIcon />}
            onClick={() => logout()}
            sx={{ borderColor: '#334155' }}
          >
            Sign Out
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
