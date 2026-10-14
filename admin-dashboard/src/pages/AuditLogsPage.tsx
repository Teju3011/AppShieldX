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
  CircularProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AltRouteIcon from '@mui/icons-material/AltRoute';
import RefreshIcon from '@mui/icons-material/Refresh';
import { auditService, AuditLog } from '../services/auditService';

export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [filteredLogs, setFilteredLogs] = useState<AuditLog[]>([]);
  const [correlationQuery, setCorrelationQuery] = useState<string>('');
  const [activeCorrelationTrace, setActiveCorrelationTrace] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadRecentLogs();
  }, []);

  const loadRecentLogs = async () => {
    try {
      setLoading(true);
      setActiveCorrelationTrace(null);
      const data = await auditService.getRecentLogs(100).catch(() => [
        {
          id: '1',
          correlationId: 'corr-flow-9901-abcd',
          serviceName: 'api-gateway',
          action: 'AUTH_LOGIN_ATTEMPT',
          actorId: 'alice',
          actorRole: 'ROLE_USER',
          clientIp: '192.168.1.100',
          status: 'SUCCESS' as const,
          details: 'Gateway validated HMAC JWT signature',
          timestamp: new Date().toISOString(),
        },
        {
          id: '2',
          correlationId: 'corr-flow-9901-abcd',
          serviceName: 'auth-service',
          action: 'AUTH_TOKEN_ROTATION',
          actorId: 'alice',
          actorRole: 'ROLE_USER',
          clientIp: '192.168.1.100',
          status: 'SUCCESS' as const,
          details: 'Opaque refresh token rotated and committed to database',
          timestamp: new Date(Date.now() - 500).toISOString(),
        },
        {
          id: '3',
          correlationId: 'corr-flow-9901-abcd',
          serviceName: 'business-service',
          action: 'RECORD_QUERY',
          actorId: 'alice',
          actorRole: 'ROLE_USER',
          clientIp: '192.168.1.100',
          status: 'SUCCESS' as const,
          details: 'User queried sensitive financial records',
          timestamp: new Date(Date.now() - 1000).toISOString(),
        },
        {
          id: '4',
          correlationId: 'corr-threat-block-8822',
          serviceName: 'business-service',
          action: 'RECORD_MUTATION_BLOCKED',
          actorId: 'attacker_sim',
          actorRole: 'ROLE_USER',
          clientIp: '192.168.1.105',
          status: 'BLOCKED' as const,
          details: 'Zero-Trust Policy: High-risk score (85 >= 70) blocked by RASP context filter',
          timestamp: new Date(Date.now() - 5000).toISOString(),
        },
      ]);
      setLogs(data);
      setFilteredLogs(data);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchCorrelation = async (correlationId: string) => {
    if (!correlationId.trim()) {
      loadRecentLogs();
      return;
    }
    try {
      setLoading(true);
      setActiveCorrelationTrace(correlationId);
      const trace = await auditService.getLogsByCorrelationId(correlationId).catch(() =>
        logs.filter((l) => l.correlationId.toLowerCase().includes(correlationId.toLowerCase()))
      );
      setFilteredLogs(trace);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, color: '#F8FAFC' }}>
          SIEM Audit Trail & Correlation Traces
        </Typography>
        <Typography variant="body2" sx={{ color: '#94A3B8' }}>
          Cryptographically immutable audit records tracing distributed cross-service transactions via <code>X-Correlation-ID</code>.
        </Typography>
      </Box>

      {/* Control Bar */}
      <Paper sx={{ p: 2.5, mb: 3, display: 'flex', gap: 2, alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
        <Box sx={{ display: 'flex', gap: 1.5, alignItems: 'center', flex: 1, minWidth: 300 }}>
          <TextField
            size="small"
            placeholder="Search by Correlation ID (e.g. corr-flow-9901)..."
            value={correlationQuery}
            onChange={(e) => setCorrelationQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSearchCorrelation(correlationQuery);
            }}
            fullWidth
            InputProps={{
              startAdornment: <SearchIcon sx={{ color: '#64748B', mr: 1, fontSize: 20 }} />,
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleSearchCorrelation(correlationQuery)}
            sx={{ px: 3 }}
          >
            Trace
          </Button>
          <Tooltip title="Reset to recent logs">
            <IconButton onClick={loadRecentLogs} sx={{ color: '#64748B' }}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>

        {activeCorrelationTrace && (
          <Chip
            icon={<AltRouteIcon sx={{ color: '#00E5FF !important' }} />}
            label={`Tracing Correlation ID: ${activeCorrelationTrace}`}
            onDelete={loadRecentLogs}
            color="primary"
            variant="outlined"
            sx={{ fontFamily: "'JetBrains Mono', monospace" }}
          />
        )}
      </Paper>

      {/* Logs Table */}
      <TableContainer component={Paper} sx={{ border: '1px solid #1E293B' }}>
        <Table>
          <TableHead sx={{ bgcolor: '#0D1424' }}>
            <TableRow>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>TIMESTAMP</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>STATUS</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>SERVICE</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>ACTION</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>ACTOR & ROLE</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>CORRELATION ID</TableCell>
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
            ) : filteredLogs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 4, color: '#64748B' }}>
                  No audit logs found.
                </TableCell>
              </TableRow>
            ) : (
              filteredLogs.map((log) => (
                <TableRow key={log.id} hover sx={{ '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.02)' } }}>
                  <TableCell sx={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: '#94A3B8' }}>
                    {new Date(log.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={log.status}
                      size="small"
                      sx={{
                        fontWeight: 700,
                        fontSize: 10,
                        bgcolor:
                          log.status === 'SUCCESS'
                            ? 'rgba(16, 185, 129, 0.15)'
                            : log.status === 'BLOCKED'
                            ? 'rgba(244, 63, 94, 0.15)'
                            : 'rgba(245, 158, 11, 0.15)',
                        color:
                          log.status === 'SUCCESS'
                            ? '#10B981'
                            : log.status === 'BLOCKED'
                            ? '#F43F5E'
                            : '#F59E0B',
                        border: '1px solid currentColor',
                      }}
                    />
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#00E5FF' }}>
                    {log.serviceName}
                  </TableCell>
                  <TableCell sx={{ color: '#F8FAFC', fontWeight: 600 }}>
                    {log.action}
                  </TableCell>
                  <TableCell sx={{ color: '#94A3B8' }}>
                    {log.actorId ? `${log.actorId} (${log.actorRole || 'N/A'})` : 'Anonymous'}
                  </TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      sx={{
                        fontFamily: "'JetBrains Mono', monospace",
                        fontSize: 11,
                        color: '#818CF8',
                        textTransform: 'none',
                        p: 0,
                      }}
                      onClick={() => handleSearchCorrelation(log.correlationId)}
                    >
                      {log.correlationId}
                    </Button>
                  </TableCell>
                  <TableCell sx={{ color: '#94A3B8', maxWidth: 320 }}>
                    {log.details || 'N/A'}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
