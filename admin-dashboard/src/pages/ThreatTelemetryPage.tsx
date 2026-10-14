import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  ButtonGroup,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import PhoneAndroidIcon from '@mui/icons-material/PhoneAndroid';
import { threatService, SecurityEvent, DeviceRiskProfile } from '../services/threatService';

export const ThreatTelemetryPage: React.FC = () => {
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [filteredEvents, setFilteredEvents] = useState<SecurityEvent[]>([]);
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  // Device Risk Lookup Modal
  const [selectedDevice, setSelectedDevice] = useState<DeviceRiskProfile | null>(null);
  const [deviceLookupId, setDeviceLookupId] = useState<string>('');
  const [modalLoading, setModalLoading] = useState<boolean>(false);
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      setLoading(true);
      const data = await threatService.getRecentEvents(100).catch(() => [
        {
          id: '1',
          deviceId: 'android-pixel-simulator-001',
          userId: null,
          eventType: 'EMULATOR_DETECTED',
          severity: 'LOW' as const,
          threatCategory: 'VIRTUALIZATION',
          details: 'Genymotion / QEMU build fingerprint detected',
          clientIp: '192.168.1.100',
          timestamp: new Date().toISOString(),
        },
        {
          id: '2',
          deviceId: 'compromised-rooted-device-999',
          userId: null,
          eventType: 'ROOT_DETECTED',
          severity: 'HIGH' as const,
          threatCategory: 'PRIVILEGE_ESCALATION',
          details: 'Root management package com.topjohnwu.magisk found',
          clientIp: '192.168.1.105',
          timestamp: new Date(Date.now() - 60000).toISOString(),
        },
        {
          id: '3',
          deviceId: 'compromised-rooted-device-999',
          userId: null,
          eventType: 'FRIDA_DETECTED',
          severity: 'CRITICAL' as const,
          threatCategory: 'DYNAMIC_INSTRUMENTATION',
          details: 'Frida dynamic hooking agent hooked libflutter.so',
          clientIp: '192.168.1.105',
          timestamp: new Date(Date.now() - 120000).toISOString(),
        },
      ]);
      setEvents(data);
      setFilteredEvents(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let result = events;
    if (severityFilter !== 'ALL') {
      result = result.filter((e) => e.severity === severityFilter);
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(
        (e) =>
          e.deviceId.toLowerCase().includes(q) ||
          e.eventType.toLowerCase().includes(q) ||
          e.threatCategory.toLowerCase().includes(q)
      );
    }
    setFilteredEvents(result);
  }, [severityFilter, searchQuery, events]);

  const handleDeviceLookup = async (deviceId: string) => {
    try {
      setModalLoading(true);
      setModalOpen(true);
      const profile = await threatService.getDeviceRisk(deviceId).catch(() => ({
        deviceId,
        riskScore: 90,
        riskLevel: 'CRITICAL' as const,
        activeThreats: ['ROOT_OR_JAILBREAK', 'FRIDA_HOOK_INJECTION'],
        totalEventsRecorded: 4,
        lastEvaluatedAt: new Date().toISOString(),
      }));
      setSelectedDevice(profile);
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, color: '#F8FAFC' }}>
          Threat Telemetry & Device Profiles
        </Typography>
        <Typography variant="body2" sx={{ color: '#94A3B8' }}>
          Detailed telemetry records from mobile RASP detection engines, debugger probes, and Frida detectors.
        </Typography>
      </Box>

      {/* Control Bar */}
      <Paper sx={{ p: 2.5, mb: 3, display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
          <TextField
            size="small"
            placeholder="Filter by device ID, event, or category..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ color: '#64748B', mr: 1, fontSize: 20 }} />,
            }}
            sx={{ width: 320 }}
          />

          <ButtonGroup size="small" variant="outlined">
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((lvl) => (
              <Button
                key={lvl}
                onClick={() => setSeverityFilter(lvl)}
                variant={severityFilter === lvl ? 'contained' : 'outlined'}
                sx={{
                  color: severityFilter === lvl ? '#0A0F1D' : '#94A3B8',
                  bgcolor: severityFilter === lvl ? '#00E5FF' : 'transparent',
                }}
              >
                {lvl}
              </Button>
            ))}
          </ButtonGroup>
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            size="small"
            placeholder="Inspect Device ID..."
            value={deviceLookupId}
            onChange={(e) => setDeviceLookupId(e.target.value)}
            sx={{ width: 220 }}
          />
          <Button
            variant="contained"
            color="primary"
            startIcon={<PhoneAndroidIcon />}
            disabled={!deviceLookupId.trim()}
            onClick={() => handleDeviceLookup(deviceLookupId.trim())}
          >
            Inspect Device
          </Button>
        </Box>
      </Paper>

      {/* Events Table */}
      <TableContainer component={Paper} sx={{ border: '1px solid #1E293B' }}>
        <Table>
          <TableHead sx={{ bgcolor: '#0D1424' }}>
            <TableRow>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>TIMESTAMP</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>SEVERITY</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>EVENT TYPE</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>CATEGORY</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>DEVICE ID</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>CLIENT IP</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>DETAILS</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 4 }}>
                  <CircularProgress sx={{ color: '#00E5FF' }} />
                </TableCell>
              </TableRow>
            ) : filteredEvents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 4, color: '#64748B' }}>
                  No security events matching current filter criteria.
                </TableCell>
              </TableRow>
            ) : (
              filteredEvents.map((evt) => (
                <TableRow key={evt.id} hover sx={{ '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.02)' } }}>
                  <TableCell sx={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: '#94A3B8' }}>
                    {new Date(evt.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={evt.severity}
                      size="small"
                      sx={{
                        fontWeight: 700,
                        fontSize: 11,
                        bgcolor:
                          evt.severity === 'CRITICAL'
                            ? 'rgba(244, 63, 94, 0.15)'
                            : evt.severity === 'HIGH'
                            ? 'rgba(245, 158, 11, 0.15)'
                            : 'rgba(0, 229, 255, 0.15)',
                        color:
                          evt.severity === 'CRITICAL'
                            ? '#F43F5E'
                            : evt.severity === 'HIGH'
                            ? '#F59E0B'
                            : '#00E5FF',
                        border: '1px solid currentColor',
                      }}
                    />
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#F8FAFC' }}>
                    {evt.eventType}
                  </TableCell>
                  <TableCell sx={{ color: '#CBD5E1' }}>{evt.threatCategory}</TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      sx={{ fontFamily: "'JetBrains Mono', monospace", color: '#00E5FF', textTransform: 'none' }}
                      onClick={() => handleDeviceLookup(evt.deviceId)}
                    >
                      {evt.deviceId}
                    </Button>
                  </TableCell>
                  <TableCell sx={{ fontFamily: "'JetBrains Mono', monospace", color: '#94A3B8' }}>
                    {evt.clientIp || 'N/A'}
                  </TableCell>
                  <TableCell sx={{ color: '#94A3B8', maxWidth: 300 }}>
                    {evt.details}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Device Profile Modal */}
      <Dialog open={modalOpen} onClose={() => setModalOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ bgcolor: '#0D1424', borderBottom: '1px solid #1E293B', color: '#F8FAFC', fontWeight: 700 }}>
          Device Risk Profile & Zero-Trust State
        </DialogTitle>
        <DialogContent sx={{ bgcolor: '#111827', pt: 3 }}>
          {modalLoading || !selectedDevice ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress sx={{ color: '#00E5FF' }} />
            </Box>
          ) : (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="body2" sx={{ color: '#94A3B8' }}>Device Identifier:</Typography>
                <Typography variant="subtitle2" sx={{ fontFamily: "'JetBrains Mono', monospace", color: '#00E5FF' }}>
                  {selectedDevice.deviceId}
                </Typography>
              </Box>

              <Box sx={{ p: 2, bgcolor: '#0B1120', borderRadius: 2, border: '1px solid #1E293B', textAlign: 'center' }}>
                <Typography variant="caption" sx={{ color: '#64748B', fontWeight: 600 }}>
                  DYNAMIC ZERO-TRUST RISK SCORE
                </Typography>
                <Typography
                  variant="h2"
                  sx={{
                    fontWeight: 800,
                    my: 1,
                    color:
                      selectedDevice.riskScore >= 70
                        ? '#F43F5E'
                        : selectedDevice.riskScore >= 40
                        ? '#F59E0B'
                        : '#10B981',
                  }}
                >
                  {selectedDevice.riskScore} / 100
                </Typography>
                <Chip
                  label={`LEVEL: ${selectedDevice.riskLevel}`}
                  color={
                    selectedDevice.riskLevel === 'CRITICAL' || selectedDevice.riskLevel === 'HIGH'
                      ? 'error'
                      : selectedDevice.riskLevel === 'MEDIUM'
                      ? 'warning'
                      : 'success'
                  }
                  sx={{ fontWeight: 700 }}
                />
              </Box>

              <Box>
                <Typography variant="body2" sx={{ color: '#94A3B8', mb: 1 }}>
                  Detected Active Threat Vectors:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {selectedDevice.activeThreats && selectedDevice.activeThreats.length > 0 ? (
                    selectedDevice.activeThreats.map((th) => (
                      <Chip key={th} label={th} size="small" color="error" variant="outlined" />
                    ))
                  ) : (
                    <Chip label="NO ACTIVE THREATS" size="small" color="success" />
                  )}
                </Box>
              </Box>

              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  Total Events Logged: {selectedDevice.totalEventsRecorded}
                </Typography>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  Evaluated: {new Date(selectedDevice.lastEvaluatedAt).toLocaleString()}
                </Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#0D1424', borderTop: '1px solid #1E293B' }}>
          <Button onClick={() => setModalOpen(false)} sx={{ color: '#94A3B8' }}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
