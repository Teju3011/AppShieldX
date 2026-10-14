import React, { useState } from 'react';
import { Box, Paper, Typography, TextField, Button, Alert, CircularProgress } from '@mui/material';
import ShieldIcon from '@mui/icons-material/Shield';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState<string>('admin@enterprise.internal');
  const [password, setPassword] = useState<string>('AdminP@ssw0rd2026!');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      await login(email, password);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        bgcolor: '#0A0F1D',
        p: 2,
      }}
    >
      <Paper
        elevation={0}
        sx={{
          p: 4,
          width: '100%',
          maxWidth: 440,
          bgcolor: '#111827',
          border: '1px solid #1E293B',
          borderRadius: 3,
        }}
      >
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Box
            sx={{
              display: 'inline-flex',
              p: 1.5,
              borderRadius: '50%',
              bgcolor: 'rgba(0, 229, 255, 0.1)',
              border: '1px solid rgba(0, 229, 255, 0.3)',
              mb: 1.5,
            }}
          >
            <ShieldIcon sx={{ color: '#00E5FF', fontSize: 36 }} />
          </Box>
          <Typography variant="h5" sx={{ fontWeight: 800, color: '#F8FAFC' }}>
            SECOPS CONSOLE
          </Typography>
          <Typography variant="body2" sx={{ color: '#94A3B8' }}>
            Cloud Native Security Framework Administration
          </Typography>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 2.5 }}>{error}</Alert>}

        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Administrator Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            required
            autoComplete="email"
          />

          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            required
            autoComplete="current-password"
          />

          <Button
            type="submit"
            variant="contained"
            color="primary"
            size="large"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <LockOpenIcon />}
            sx={{ mt: 1, py: 1.2, fontWeight: 700 }}
          >
            {loading ? 'Authenticating...' : 'Sign In to Console'}
          </Button>

          <Box sx={{ mt: 2, p: 1.5, bgcolor: '#0B1120', borderRadius: 2, border: '1px solid #1E293B' }}>
            <Typography variant="caption" sx={{ color: '#64748B', display: 'block', mb: 0.5 }}>
              DEFAULT SEED CREDENTIALS:
            </Typography>
            <Typography variant="caption" sx={{ fontFamily: "'JetBrains Mono', monospace", color: '#00E5FF', display: 'block' }}>
              admin@enterprise.internal
            </Typography>
            <Typography variant="caption" sx={{ fontFamily: "'JetBrains Mono', monospace", color: '#94A3B8' }}>
              AdminP@ssw0rd2026!
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};
