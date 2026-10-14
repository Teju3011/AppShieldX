import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Divider,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import TuneIcon from '@mui/icons-material/Tune';
import SaveIcon from '@mui/icons-material/Save';
import RefreshIcon from '@mui/icons-material/Refresh';
import SecurityIcon from '@mui/icons-material/Security';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import { threatService } from '../services/threatService';

export const PolicyManagementPage: React.FC = () => {
  const [configs, setConfigs] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [alertMsg, setAlertMsg] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const fetchConfigs = async () => {
    try {
      setLoading(true);
      const data = await threatService.getPolicyConfigurations();
      setConfigs(data);
    } catch (err) {
      console.error('Failed to load policy configurations:', err);
      setAlertMsg({ type: 'error', message: 'Failed to retrieve server policy configurations.' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfigs();
  }, []);

  const handleChange = (key: string, value: string) => {
    setConfigs((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      const updated = await threatService.updatePolicyConfigurations(configs);
      setConfigs(updated);
      setAlertMsg({ type: 'success', message: 'Server-side risk policies and weights updated successfully.' });
    } catch (err) {
      console.error('Failed to update policies:', err);
      setAlertMsg({ type: 'error', message: 'Failed to persist policy updates to backend.' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <AdminPanelSettingsIcon sx={{ color: '#00E5FF', fontSize: 30 }} />
            <Typography variant="h5" sx={{ fontWeight: 700, color: '#F8FAFC' }}>
              Adaptive Security Policy & Risk Threshold Management
            </Typography>
          </Box>
          <Typography variant="body2" sx={{ color: '#94A3B8', mt: 0.5 }}>
            Restricted administrator interface for configuring authoritative risk scoring weights, response bands, and correlation windows.
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1.5 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchConfigs}
            disabled={loading}
            sx={{ borderColor: '#334155', color: '#00E5FF' }}
          >
            Reset
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={saving || loading}
            sx={{ bgcolor: '#00E5FF', color: '#0D1424', fontWeight: 700, '&:hover': { bgcolor: '#00B4D8' } }}
          >
            {saving ? 'Saving...' : 'Deploy Policy'}
          </Button>
        </Box>
      </Box>

      {alertMsg && (
        <Alert severity={alertMsg.type} sx={{ mb: 3 }} onClose={() => setAlertMsg(null)}>
          {alertMsg.message}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
          <CircularProgress sx={{ color: '#00E5FF' }} />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {/* Response Bands */}
          <Grid item xs={12} md={5}>
            <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <SecurityIcon sx={{ color: '#00E5FF' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600, color: '#F8FAFC' }}>
                    Authoritative Response Bands
                  </Typography>
                </Box>
                <Typography variant="body2" sx={{ color: '#94A3B8', mb: 3 }}>
                  Normalized risk scores (0–100) are evaluated against server-defined response bands:
                </Typography>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
                  <Box sx={{ bgcolor: '#111827', p: 2, borderRadius: 2, border: '1px solid #1E293B' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Chip label="ALLOW" color="success" size="small" sx={{ fontWeight: 700 }} />
                      <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                        Score: 0 to {configs['risk.bands.allow_max'] || '24'}
                      </Typography>
                    </Box>
                    <Typography variant="caption" sx={{ color: '#64748B' }}>
                      Standard access granted for authorized sessions. Zero disruption to verified users.
                    </Typography>
                  </Box>

                  <Box sx={{ bgcolor: '#111827', p: 2, borderRadius: 2, border: '1px solid #1E293B' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Chip label="MONITOR" color="info" size="small" sx={{ fontWeight: 700 }} />
                      <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                        Score: {(parseInt(configs['risk.bands.allow_max'] || '24') + 1)} to {configs['risk.bands.monitor_max'] || '49'}
                      </Typography>
                    </Box>
                    <Typography variant="caption" sx={{ color: '#64748B' }}>
                      Audit logging and enhanced SOC telemetry without interrupting normal user interactions.
                    </Typography>
                  </Box>

                  <Box sx={{ bgcolor: '#111827', p: 2, borderRadius: 2, border: '1px solid #1E293B' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Chip label="STEP_UP_AUTHENTICATION" color="warning" size="small" sx={{ fontWeight: 700 }} />
                      <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                        Score: {(parseInt(configs['risk.bands.monitor_max'] || '49') + 1)} to {configs['risk.bands.step_up_max'] || '74'}
                      </Typography>
                    </Box>
                    <Typography variant="caption" sx={{ color: '#64748B' }}>
                      Requires secondary verified MFA/Step-up verification before executing sensitive business requests.
                    </Typography>
                  </Box>

                  <Box sx={{ bgcolor: '#111827', p: 2, borderRadius: 2, border: '1px solid #1E293B' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Chip label="RESTRICT_SENSITIVE_ACTIONS" color="error" size="small" sx={{ fontWeight: 700 }} />
                      <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                        Score: {(parseInt(configs['risk.bands.step_up_max'] || '74') + 1)} to 100
                      </Typography>
                    </Box>
                    <Typography variant="caption" sx={{ color: '#64748B' }}>
                      Server-side 403 Forbidden enforcement on state-modifying endpoints (POST, PUT, DELETE).
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Scoring Weights & Sliding Windows */}
          <Grid item xs={12} md={7}>
            <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2, mb: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <TuneIcon sx={{ color: '#00E5FF' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600, color: '#F8FAFC' }}>
                    Threat Scoring Weights & Multipliers
                  </Typography>
                </Box>
                <Typography variant="body2" sx={{ color: '#94A3B8', mb: 3 }}>
                  Configure point additions for detected threat indicators and cross-layer combinations:
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Root / Jailbreak Weight"
                      value={configs['risk.weights.root_jailbreak'] || ''}
                      onChange={(e) => handleChange('risk.weights.root_jailbreak', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Frida Dynamic Hook Weight"
                      value={configs['risk.weights.frida_hook'] || ''}
                      onChange={(e) => handleChange('risk.weights.frida_hook', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Debugger Attached Weight"
                      value={configs['risk.weights.debugger'] || ''}
                      onChange={(e) => handleChange('risk.weights.debugger', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Package Tampering Weight"
                      value={configs['risk.weights.signature_tamper'] || ''}
                      onChange={(e) => handleChange('risk.weights.signature_tamper', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Virtual Device / Emulator Weight"
                      value={configs['risk.weights.emulator'] || ''}
                      onChange={(e) => handleChange('risk.weights.emulator', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="API Auth Failure Weight"
                      value={configs['risk.weights.auth_failure'] || ''}
                      onChange={(e) => handleChange('risk.weights.auth_failure', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Authorization Denial Weight"
                      value={configs['risk.weights.authz_denial'] || ''}
                      onChange={(e) => handleChange('risk.weights.authz_denial', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Rate Limit Burst Weight"
                      value={configs['risk.weights.rate_limit_burst'] || ''}
                      onChange={(e) => handleChange('risk.weights.rate_limit_burst', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Cross-Layer Correlation Synergy Bonus"
                      value={configs['risk.weights.cross_layer_bonus'] || ''}
                      onChange={(e) => handleChange('risk.weights.cross_layer_bonus', e.target.value)}
                      helperText="Bounded additional risk contribution when multi-layer indicators coincide on verified session"
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            {/* Sliding Windows */}
            <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, color: '#F8FAFC', mb: 2 }}>
                  Temporal Windows & Deduplication TTL
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Correlation Window (Seconds)"
                      value={configs['correlation.sliding_window_seconds'] || ''}
                      onChange={(e) => handleChange('correlation.sliding_window_seconds', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      size="small"
                      label="Deduplication Hash TTL (Seconds)"
                      value={configs['correlation.dedup_ttl_seconds'] || ''}
                      onChange={(e) => handleChange('correlation.dedup_ttl_seconds', e.target.value)}
                      sx={{ input: { color: '#F8FAFC' } }}
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};
