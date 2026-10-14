import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider,
} from '@mui/material';
import HubIcon from '@mui/icons-material/Hub';
import RefreshIcon from '@mui/icons-material/Refresh';
import ShieldIcon from '@mui/icons-material/Shield';
import SecurityIcon from '@mui/icons-material/Security';
import TimelineIcon from '@mui/icons-material/Timeline';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { threatService, CorrelationResult } from '../services/threatService';

export const CorrelationPage: React.FC = () => {
  const [correlations, setCorrelations] = useState<CorrelationResult[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedCorrelation, setSelectedCorrelation] = useState<CorrelationResult | null>(null);

  const fetchCorrelations = async () => {
    try {
      setLoading(true);
      const data = await threatService.getCorrelations(50);
      setCorrelations(data);
    } catch (err) {
      console.error('Failed to load correlations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCorrelations();
    const interval = setInterval(fetchCorrelations, 15000);
    return () => clearInterval(interval);
  }, []);

  const getActionColor = (action: string) => {
    switch (action) {
      case 'RESTRICT_SENSITIVE_ACTIONS':
        return 'error';
      case 'STEP_UP_AUTHENTICATION':
        return 'warning';
      case 'MONITOR':
        return 'info';
      default:
        return 'success';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <HubIcon sx={{ color: '#00E5FF', fontSize: 30 }} />
            <Typography variant="h5" sx={{ fontWeight: 700, color: '#F8FAFC' }}>
              Cross-Layer Threat Correlation Engine
            </Typography>
          </Box>
          <Typography variant="body2" sx={{ color: '#94A3B8', mt: 0.5 }}>
            Real-time correlation of mobile client runtime telemetry (Android/iOS) and backend API behavior across sliding time windows.
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchCorrelations}
          disabled={loading}
          sx={{ borderColor: '#334155', color: '#00E5FF' }}
        >
          Refresh Feed
        </Button>
      </Box>

      {/* Summary KPI Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
            <CardContent>
              <Typography variant="overline" sx={{ color: '#64748B', fontWeight: 700 }}>
                CORRELATED DECISIONS
              </Typography>
              <Typography variant="h4" sx={{ color: '#00E5FF', fontWeight: 700, mt: 0.5 }}>
                {correlations.length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                Sliding window evaluations
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
            <CardContent>
              <Typography variant="overline" sx={{ color: '#64748B', fontWeight: 700 }}>
                RESTRICTED SESSIONS
              </Typography>
              <Typography variant="h4" sx={{ color: '#FF1744', fontWeight: 700, mt: 0.5 }}>
                {correlations.filter((c) => c.finalEnforcedAction === 'RESTRICT_SENSITIVE_ACTIONS').length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                High-risk policy blocks
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
            <CardContent>
              <Typography variant="overline" sx={{ color: '#64748B', fontWeight: 700 }}>
                STEP-UP CHALLENGES
              </Typography>
              <Typography variant="h4" sx={{ color: '#FF9100', fontWeight: 700, mt: 0.5 }}>
                {correlations.filter((c) => c.finalEnforcedAction === 'STEP_UP_AUTHENTICATION').length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                Adaptive authentication required
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
            <CardContent>
              <Typography variant="overline" sx={{ color: '#64748B', fontWeight: 700 }}>
                DEDUP REPLAYS MITIGATED
              </Typography>
              <Typography variant="h4" sx={{ color: '#00E676', fontWeight: 700, mt: 0.5 }}>
                {correlations.filter((c) => c.correlationRuleId === 'RULE-CORR-04').length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                Unbounded score inflation prevented
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Correlation Timeline & Evidence Feed */}
      <Card sx={{ bgcolor: '#0D1424', border: '1px solid #1E293B', borderRadius: 2 }}>
        <CardContent sx={{ p: 0 }}>
          <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <TimelineIcon sx={{ color: '#00E5FF' }} />
            <Typography variant="h6" sx={{ fontWeight: 600, color: '#F8FAFC' }}>
              Multi-Layer Threat Correlation Event Stream
            </Typography>
          </Box>
          <TableContainer>
            <Table size="small">
              <TableHead sx={{ bgcolor: '#111827' }}>
                <TableRow>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>TIMESTAMP</TableCell>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>CORRELATION ID</TableCell>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>RULE MATCHED</TableCell>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>PLATFORM</TableCell>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>RISK DELTA</TableCell>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>ENFORCED ACTION</TableCell>
                  <TableCell sx={{ color: '#64748B', fontWeight: 600 }}>EVIDENCE</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading && correlations.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} sx={{ textAlign: 'center', py: 4 }}>
                      <CircularProgress size={24} sx={{ color: '#00E5FF' }} />
                    </TableCell>
                  </TableRow>
                ) : correlations.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} sx={{ textAlign: 'center', py: 4, color: '#64748B' }}>
                      No cross-layer correlation events recorded yet. Run test scenarios to generate multi-layer events.
                    </TableCell>
                  </TableRow>
                ) : (
                  correlations.map((row) => (
                    <TableRow key={row.correlationId} sx={{ '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' } }}>
                      <TableCell sx={{ color: '#94A3B8', fontSize: '0.8rem' }}>
                        {new Date(row.timestamp).toLocaleTimeString()}
                      </TableCell>
                      <TableCell sx={{ color: '#F8FAFC', fontFamily: 'monospace', fontSize: '0.78rem' }}>
                        {row.correlationId.substring(0, 12)}...
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={row.correlationRuleId}
                          size="small"
                          sx={{
                            bgcolor: row.correlationRuleId.includes('CORR') ? 'rgba(0, 229, 255, 0.1)' : 'rgba(148, 163, 184, 0.1)',
                            color: row.correlationRuleId.includes('CORR') ? '#00E5FF' : '#94A3B8',
                            fontWeight: 600,
                            fontSize: '0.75rem',
                          }}
                        />
                      </TableCell>
                      <TableCell sx={{ color: '#94A3B8', fontSize: '0.8rem' }}>{row.platform}</TableCell>
                      <TableCell sx={{ color: '#F8FAFC', fontSize: '0.85rem' }}>
                        <Typography component="span" sx={{ color: '#64748B' }}>
                          {row.riskScoreBefore}
                        </Typography>
                        {' → '}
                        <Typography
                          component="span"
                          sx={{
                            fontWeight: 700,
                            color: row.riskScoreAfter >= 75 ? '#FF1744' : row.riskScoreAfter >= 50 ? '#FF9100' : '#00E676',
                          }}
                        >
                          {row.riskScoreAfter}
                        </Typography>
                        {row.riskContribution > 0 && (
                          <Typography component="span" sx={{ color: '#FF9100', fontSize: '0.75rem', ml: 0.5 }}>
                            (+{row.riskContribution})
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={row.finalEnforcedAction}
                          size="small"
                          color={getActionColor(row.finalEnforcedAction)}
                          sx={{ fontWeight: 700, fontSize: '0.72rem' }}
                        />
                      </TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          variant="text"
                          startIcon={<VisibilityIcon fontSize="small" />}
                          onClick={() => setSelectedCorrelation(row)}
                          sx={{ color: '#00E5FF', fontSize: '0.75rem' }}
                        >
                          Inspect
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Evidence Inspection Modal */}
      {selectedCorrelation && (
        <Dialog
          open={!!selectedCorrelation}
          onClose={() => setSelectedCorrelation(null)}
          maxWidth="md"
          fullWidth
          PaperProps={{ sx: { bgcolor: '#0D1424', border: '1px solid #1E293B', color: '#F8FAFC' } }}
        >
          <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ShieldIcon sx={{ color: '#00E5FF' }} />
            Threat Correlation Evidence Inspector
          </DialogTitle>
          <DialogContent dividers sx={{ borderColor: '#1E293B' }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  CORRELATION ID
                </Typography>
                <Typography sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                  {selectedCorrelation.correlationId}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  RULE APPLIED
                </Typography>
                <Typography sx={{ fontWeight: 600, color: '#00E5FF' }}>
                  {selectedCorrelation.correlationRuleId}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  TIME WINDOW
                </Typography>
                <Typography>{selectedCorrelation.timeWindowSeconds} seconds sliding window</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  CONFIDENCE
                </Typography>
                <Typography sx={{ color: '#00E676', fontWeight: 600 }}>
                  {selectedCorrelation.confidence}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Divider sx={{ my: 1, borderColor: '#1E293B' }} />
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  EXPLANATION & SERVER REASONING
                </Typography>
                <Typography sx={{ mt: 0.5, bgcolor: '#111827', p: 1.5, borderRadius: 1, fontSize: '0.9rem' }}>
                  {selectedCorrelation.explanation}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  MATCHED CONDITIONS
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 0.5 }}>
                  {selectedCorrelation.matchedConditions.map((cond, i) => (
                    <Chip key={i} label={cond} size="small" sx={{ bgcolor: 'rgba(0, 229, 255, 0.1)', color: '#00E5FF' }} />
                  ))}
                </Box>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="caption" sx={{ color: '#64748B' }}>
                  RELATED SECURITY EVENT REFERENCES
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 0.5 }}>
                  {selectedCorrelation.relatedEventReferences.map((ref, i) => (
                    <Chip key={i} label={ref} size="small" sx={{ bgcolor: '#1E293B', color: '#94A3B8', fontFamily: 'monospace' }} />
                  ))}
                </Box>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions sx={{ p: 2, borderColor: '#1E293B' }}>
            <Button onClick={() => setSelectedCorrelation(null)} sx={{ color: '#00E5FF' }}>
              Close
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  );
};
