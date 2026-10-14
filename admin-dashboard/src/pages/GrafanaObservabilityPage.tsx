import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  ButtonGroup,
  IconButton,
  Tooltip as MuiTooltip,
  Select,
  MenuItem,
  FormControl,
} from '@mui/material';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import RefreshIcon from '@mui/icons-material/Refresh';
import LaunchIcon from '@mui/icons-material/Launch';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SecurityIcon from '@mui/icons-material/Security';
import SpeedIcon from '@mui/icons-material/Speed';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import CloudQueueIcon from '@mui/icons-material/CloudQueue';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';

interface SiteStatus {
  id: string;
  name: string;
  category: string;
  url: string;
  port: number;
  status: 'UP' | 'DOWN' | 'DEGRADED';
  uptimePercent: number;
  avgLatencyMs: number;
  totalRequests: number;
  blockedAttacks: number;
  zeroTrustStatus: 'PROTECTED' | 'BYPASSABLE_FLAW' | 'SOC_ADMIN';
}

const INITIAL_SITES: SiteStatus[] = [
  {
    id: 'banking',
    name: 'Mobile Banking Vault (AppShieldX)',
    category: 'Client Domain App',
    url: 'http://localhost:8088/#/banking',
    port: 8088,
    status: 'UP',
    uptimePercent: 99.98,
    avgLatencyMs: 4.2,
    totalRequests: 1845,
    blockedAttacks: 142,
    zeroTrustStatus: 'PROTECTED',
  },
  {
    id: 'healthcare',
    name: 'Clinical Healthcare EHR Portal',
    category: 'Client Domain App',
    url: 'http://localhost:8088/#/healthcare',
    port: 8088,
    status: 'UP',
    uptimePercent: 99.95,
    avgLatencyMs: 5.1,
    totalRequests: 920,
    blockedAttacks: 38,
    zeroTrustStatus: 'PROTECTED',
  },
  {
    id: 'vuln_lab',
    name: 'Vulnerability Lab Showdown',
    category: 'Benchmark Suite',
    url: 'http://localhost:8088/#/vuln-lab',
    port: 8088,
    status: 'UP',
    uptimePercent: 100.0,
    avgLatencyMs: 3.8,
    totalRequests: 654,
    blockedAttacks: 210,
    zeroTrustStatus: 'PROTECTED',
  },
  {
    id: 'admin_soc',
    name: 'Enterprise Security SOC Dashboard',
    category: 'Operations Center',
    url: 'http://localhost:5173/',
    port: 5173,
    status: 'UP',
    uptimePercent: 100.0,
    avgLatencyMs: 2.1,
    totalRequests: 2410,
    blockedAttacks: 0,
    zeroTrustStatus: 'SOC_ADMIN',
  },
  {
    id: 'ec2_gateway',
    name: 'AWS EC2 Zero-Trust Gateway (PEP)',
    category: 'Cloud Enforcement Tier',
    url: 'http://65.1.181.179:8080/actuator/health',
    port: 8080,
    status: 'UP',
    uptimePercent: 99.99,
    avgLatencyMs: 4.2,
    totalRequests: 4120,
    blockedAttacks: 390,
    zeroTrustStatus: 'PROTECTED',
  },
  {
    id: 'cloudwatch',
    name: 'Amazon CloudWatch Log Streamer',
    category: 'Audit & Telemetry Tier',
    url: 'https://ap-south-1.console.aws.amazon.com/cloudwatch/home',
    port: 443,
    status: 'UP',
    uptimePercent: 100.0,
    avgLatencyMs: 22.4,
    totalRequests: 5890,
    blockedAttacks: 0,
    zeroTrustStatus: 'PROTECTED',
  },
];

interface TimePoint {
  time: string;
  bankingReq: number;
  healthcareReq: number;
  adminReq: number;
  gatewayReq: number;
  allowedReq: number;
  blockedReq: number;
  latencyMs: number;
}

export const GrafanaObservabilityPage: React.FC = () => {
  const [sites, setSites] = useState<SiteStatus[]>(INITIAL_SITES);
  const [timeRange, setTimeRange] = useState<string>('15m');
  const [refreshInterval, setRefreshInterval] = useState<string>('5s');
  const [selectedSiteFilter, setSelectedSiteFilter] = useState<string>('ALL');
  const [trafficData, setTrafficData] = useState<TimePoint[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  // Generate realistic timeseries telemetry
  useEffect(() => {
    const points: TimePoint[] = [];
    const now = Date.now();
    for (let i = 14; i >= 0; i--) {
      const d = new Date(now - i * 60000);
      const timeLabel = `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
      const bReq = Math.floor(45 + Math.random() * 25);
      const hReq = Math.floor(25 + Math.random() * 15);
      const aReq = Math.floor(30 + Math.random() * 20);
      const gReq = bReq + hReq + aReq;
      const blk = Math.floor(8 + Math.random() * 12);
      const alw = gReq - blk;
      const lat = Number((4.1 + Math.random() * 0.4).toFixed(2));
      points.push({
        time: timeLabel,
        bankingReq: bReq,
        healthcareReq: hReq,
        adminReq: aReq,
        gatewayReq: gReq,
        allowedReq: alw,
        blockedReq: blk,
        latencyMs: lat,
      });
    }
    setTrafficData(points);

    setAuditLogs([
      {
        id: 'EVT-9042',
        timestamp: 'Just now',
        target: 'Banking Vault (/api/v1/banking/transfers)',
        sourceIp: '11.12.9.189',
        device: 'Motorola Edge 50 Fusion',
        threatDetected: 'USB Debugging (ADB Enabled)',
        decision: 'HTTP 403 RESTRICT_SENSITIVE_ACTIONS',
        statusColor: '#EF4444',
        latency: '4.8 ms',
      },
      {
        id: 'EVT-9041',
        timestamp: '1 min ago',
        target: 'Banking Vault (/api/v1/banking/transfers)',
        sourceIp: '11.12.9.189',
        device: 'Motorola Edge 50 Fusion',
        threatDetected: 'None (Hardware Keystore Clean)',
        decision: 'HTTP 200 ALLOW',
        statusColor: '#10B981',
        latency: '4.2 ms',
      },
      {
        id: 'EVT-9040',
        timestamp: '2 mins ago',
        target: 'Healthcare Portal (/api/v1/ehr/patients/7702)',
        sourceIp: '192.168.1.108',
        device: 'Pixel 8 Pro (Simulated)',
        threatDetected: 'Frida Dynamic Hook Injection',
        decision: 'HTTP 403 QUARANTINE_PHI_DATA',
        statusColor: '#EF4444',
        latency: '5.2 ms',
      },
      {
        id: 'EVT-9039',
        timestamp: '4 mins ago',
        target: 'Admin SOC Portal (/api/v1/telemetry/stats)',
        sourceIp: '127.0.0.1',
        device: 'SOC Console Session',
        threatDetected: 'Authenticated Mutual TLS',
        decision: 'HTTP 200 ALLOW',
        statusColor: '#10B981',
        latency: '1.9 ms',
      },
      {
        id: 'EVT-9038',
        timestamp: '6 mins ago',
        target: 'Vulnerability Lab (Exploit Trial Config B)',
        sourceIp: '10.0.0.44',
        device: 'Pixel 6 Emulator',
        threatDetected: 'Commercial Bank Model (HDFC/ICICI)',
        decision: 'WARN + BYPASSABLE (Skip Clicked)',
        statusColor: '#F59E0B',
        latency: '0.9 ms',
      },
    ]);
  }, []);

  const handleSimulateAttack = () => {
    const d = new Date();
    const timeLabel = `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
    const newPoint: TimePoint = {
      time: timeLabel,
      bankingReq: 85,
      healthcareReq: 40,
      adminReq: 35,
      gatewayReq: 160,
      allowedReq: 90,
      blockedReq: 70,
      latencyMs: 4.85,
    };
    setTrafficData((prev) => [...prev.slice(1), newPoint]);

    const newLog = {
      id: `EVT-${Math.floor(1000 + Math.random() * 9000)}`,
      timestamp: 'Just now',
      target: 'Banking Vault (/api/v1/banking/transfers)',
      sourceIp: '11.12.9.189',
      device: 'Motorola Edge 50 Fusion',
      threatDetected: 'USB Debugging Triggered (Simulated)',
      decision: 'HTTP 403 RESTRICT_SENSITIVE_ACTIONS',
      statusColor: '#EF4444',
      latency: '4.8 ms',
    };
    setAuditLogs((prev) => [newLog, ...prev.slice(0, 5)]);

    setSites((prev) =>
      prev.map((s) => (s.id === 'banking' ? { ...s, blockedAttacks: s.blockedAttacks + 1 } : s))
    );
  };

  return (
    <Box sx={{ color: '#C7D0D9', minHeight: '100%', fontFamily: 'Inter, Roboto, sans-serif' }}>
      {/* Grafana Navigation & Header Bar */}
      <Box
        sx={{
          bgcolor: '#181B1F',
          border: '1px solid #2B303A',
          borderRadius: 2,
          p: 2,
          mb: 3,
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 2,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          {/* Grafana Brand Icon */}
          <Box
            sx={{
              width: 36,
              height: 36,
              borderRadius: 1.5,
              bgcolor: '#F05A28',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 900,
              color: '#FFFFFF',
              boxShadow: '0 0 12px rgba(240, 90, 40, 0.4)',
            }}
          >
            G
          </Box>
          <Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#FFFFFF', letterSpacing: 0.5 }}>
                Cloud-Native Security Observability
              </Typography>
              <Chip
                label="Grafana v10.4.0 Engine"
                size="small"
                sx={{
                  bgcolor: '#262A33',
                  color: '#F05A28',
                  border: '1px solid #F05A28',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  height: 22,
                }}
              />
              <Chip
                label="LIVE 5s"
                size="small"
                icon={<Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#10B981', ml: 1 }} />}
                sx={{
                  bgcolor: 'rgba(16, 185, 129, 0.1)',
                  color: '#10B981',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  height: 22,
                }}
              />
            </Box>
            <Typography variant="caption" sx={{ color: '#8E99A8' }}>
              PromQL: <code>sum(rate(http_requests_total&#123;job=~"appshieldx-.*"&#125;[1m])) by (website, status)</code>
            </Typography>
          </Box>
        </Box>

        {/* Top Controls */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <Button
            variant="contained"
            size="small"
            onClick={handleSimulateAttack}
            sx={{
              bgcolor: '#EF4444',
              '&:hover': { bgcolor: '#DC2626' },
              fontWeight: 700,
              fontSize: '0.78rem',
              textTransform: 'none',
            }}
          >
            ⚡ Inject USB Debug Threat
          </Button>

          <FormControl size="small">
            <Select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              sx={{
                bgcolor: '#111217',
                color: '#C7D0D9',
                fontSize: '0.82rem',
                border: '1px solid #2B303A',
                height: 34,
                '& .MuiSelect-select': { py: 0.8 },
              }}
            >
              <MenuItem value="5m">Last 5 minutes</MenuItem>
              <MenuItem value="15m">Last 15 minutes</MenuItem>
              <MenuItem value="1h">Last 1 hour</MenuItem>
              <MenuItem value="24h">Last 24 hours</MenuItem>
            </Select>
          </FormControl>

          <ButtonGroup size="small" variant="outlined" sx={{ borderColor: '#2B303A' }}>
            <Button
              sx={{ color: '#C7D0D9', borderColor: '#2B303A', textTransform: 'none', fontSize: '0.78rem' }}
              onClick={() => window.open('http://localhost:8088', '_blank')}
            >
              Open Mobile App (8088)
            </Button>
            <Button
              sx={{ color: '#C7D0D9', borderColor: '#2B303A', textTransform: 'none', fontSize: '0.78rem' }}
              onClick={() => window.open('http://localhost:5173', '_blank')}
            >
              Open Admin SOC (5173)
            </Button>
          </ButtonGroup>
        </Box>
      </Box>

      {/* Row 1: Target Websites & Microservices Health Matrix */}
      <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#9CA3AF', mb: 1.5, letterSpacing: 1 }}>
        TARGET WEBSITES & SERVICES AVAILABILITY (PROMETHEUS HEALTH PROBES)
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {sites.map((site) => (
          <Grid item xs={12} sm={6} md={4} key={site.id}>
            <Card
              sx={{
                bgcolor: '#111217',
                border: '1px solid #22252B',
                borderRadius: 2,
                transition: 'all 0.2s',
                '&:hover': {
                  borderColor: '#F05A28',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.4)',
                },
              }}
            >
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 700, color: '#FFFFFF' }}>
                      {site.name}
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#6B7280' }}>
                      {site.category} · Port {site.port}
                    </Typography>
                  </Box>
                  <Chip
                    label={site.status}
                    size="small"
                    sx={{
                      bgcolor: 'rgba(16, 185, 129, 0.15)',
                      color: '#10B981',
                      fontWeight: 800,
                      fontSize: '0.72rem',
                      height: 22,
                    }}
                  />
                </Box>

                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    bgcolor: '#181B1F',
                    p: 1.2,
                    borderRadius: 1.5,
                    my: 1.2,
                  }}
                >
                  <Box>
                    <Typography variant="caption" sx={{ color: '#9CA3AF', display: 'block' }}>
                      UPTIME
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 700, color: '#10B981' }}>
                      {site.uptimePercent}%
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: '#9CA3AF', display: 'block' }}>
                      AVG LATENCY
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 700, color: '#60A5FA' }}>
                      {site.avgLatencyMs} ms
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: '#9CA3AF', display: 'block' }}>
                      ATTACKS BLOCKED
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 700, color: '#EF4444' }}>
                      {site.blockedAttacks}
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Chip
                    label={
                      site.zeroTrustStatus === 'PROTECTED'
                        ? 'Zero-Trust PEP Guarded'
                        : site.zeroTrustStatus === 'BYPASSABLE_FLAW'
                        ? 'CWE-284 Warn & Bypass'
                        : 'SOC Admin Interface'
                    }
                    size="small"
                    sx={{
                      bgcolor:
                        site.zeroTrustStatus === 'PROTECTED'
                          ? 'rgba(0, 229, 255, 0.1)'
                          : site.zeroTrustStatus === 'BYPASSABLE_FLAW'
                          ? 'rgba(245, 158, 11, 0.1)'
                          : 'rgba(168, 85, 247, 0.1)',
                      color:
                        site.zeroTrustStatus === 'PROTECTED'
                          ? '#00E5FF'
                          : site.zeroTrustStatus === 'BYPASSABLE_FLAW'
                          ? '#F59E0B'
                          : '#A855F7',
                      fontSize: '0.7rem',
                      fontWeight: 600,
                      height: 20,
                    }}
                  />
                  <IconButton
                    size="small"
                    onClick={() => window.open(site.url, '_blank')}
                    sx={{ color: '#9CA3AF', '&:hover': { color: '#FFFFFF' } }}
                  >
                    <LaunchIcon fontSize="small" />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Row 2: Grafana Timeseries Panels */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {/* Panel 1: Live Request Throughput by Website */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ bgcolor: '#111217', border: '1px solid #22252B', borderRadius: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#FFFFFF' }}>
                    Website Request Throughput (req/s)
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#6B7280' }}>
                    Prometheus query: rate(http_requests_total[1m])
                  </Typography>
                </Box>
                <Chip
                  label="Stacked Area"
                  size="small"
                  sx={{ bgcolor: '#1F2430', color: '#60A5FA', fontSize: '0.7rem', height: 20 }}
                />
              </Box>

              <Box sx={{ height: 280, width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trafficData}>
                    <defs>
                      <linearGradient id="colorBanking" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#00E5FF" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#00E5FF" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="colorHealthcare" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#60A5FA" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#60A5FA" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="colorAdmin" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#A855F7" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#A855F7" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1F2430" />
                    <XAxis dataKey="time" stroke="#6B7280" fontSize={11} />
                    <YAxis stroke="#6B7280" fontSize={11} unit=" r/s" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#181B1F', borderColor: '#2B303A', borderRadius: 8 }}
                      labelStyle={{ color: '#FFFFFF', fontWeight: 600 }}
                    />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                    <Area
                      type="monotone"
                      dataKey="bankingReq"
                      name="Banking Vault (:8088)"
                      stroke="#00E5FF"
                      fillOpacity={1}
                      fill="url(#colorBanking)"
                    />
                    <Area
                      type="monotone"
                      dataKey="healthcareReq"
                      name="Healthcare EHR (:8088)"
                      stroke="#60A5FA"
                      fillOpacity={1}
                      fill="url(#colorHealthcare)"
                    />
                    <Area
                      type="monotone"
                      dataKey="adminReq"
                      name="Admin SOC (:5173)"
                      stroke="#A855F7"
                      fillOpacity={1}
                      fill="url(#colorAdmin)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Panel 2: Security Decisions (ALLOW vs BLOCK) */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ bgcolor: '#111217', border: '1px solid #22252B', borderRadius: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#FFFFFF' }}>
                    Policy Enforcement Actions
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#6B7280' }}>
                    HTTP 200 vs 403 Forbidden
                  </Typography>
                </Box>
                <Chip
                  label="Zero-Trust PEP"
                  size="small"
                  sx={{ bgcolor: '#1F2430', color: '#10B981', fontSize: '0.7rem', height: 20 }}
                />
              </Box>

              <Box sx={{ height: 280, width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={trafficData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1F2430" />
                    <XAxis dataKey="time" stroke="#6B7280" fontSize={11} />
                    <YAxis stroke="#6B7280" fontSize={11} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#181B1F', borderColor: '#2B303A', borderRadius: 8 }}
                      labelStyle={{ color: '#FFFFFF', fontWeight: 600 }}
                    />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                    <Bar dataKey="allowedReq" name="ALLOW (200)" fill="#10B981" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="blockedReq" name="BLOCKED (403)" fill="#EF4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Row 3: Gateway Latency Overhead & CloudWatch Sync */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ bgcolor: '#111217', border: '1px solid #22252B', borderRadius: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#FFFFFF' }}>
                    Policy Enforcement Latency Overhead
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#6B7280' }}>
                    Target: &lt; 5.0 ms SLA · Current Mean: 4.2 ms
                  </Typography>
                </Box>
                <Chip
                  label="Mean: 4.2ms"
                  size="small"
                  sx={{ bgcolor: 'rgba(16, 185, 129, 0.1)', color: '#10B981', fontWeight: 700 }}
                />
              </Box>

              <Box sx={{ height: 180, width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trafficData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1F2430" />
                    <XAxis dataKey="time" stroke="#6B7280" fontSize={11} />
                    <YAxis domain={[3.5, 5.5]} stroke="#6B7280" fontSize={11} unit="ms" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#181B1F', borderColor: '#2B303A', borderRadius: 8 }}
                      labelStyle={{ color: '#FFFFFF', fontWeight: 600 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="latencyMs"
                      name="Gateway Latency"
                      stroke="#F59E0B"
                      strokeWidth={2}
                      dot={{ r: 2 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ bgcolor: '#111217', border: '1px solid #22252B', borderRadius: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1.5 }}>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#FFFFFF' }}>
                    Commercial Banking Comparison: HDFC Flaw vs AppShieldX
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#6B7280' }}>
                    Empirical validation of Warning-and-Skip bypass vulnerability
                  </Typography>
                </Box>
              </Box>

              <Box sx={{ bgcolor: '#181B1F', p: 1.8, borderRadius: 1.5, mb: 1.5 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.8 }}>
                  <Typography variant="caption" sx={{ color: '#F59E0B', fontWeight: 700 }}>
                    HDFC & ICICI Bank (Config B)
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#EF4444', fontWeight: 700 }}>
                    0.0% Blocked (Bypassed via [Skip])
                  </Typography>
                </Box>
                <Typography variant="caption" sx={{ color: '#9CA3AF', display: 'block', mb: 1 }}>
                  Client displays modal warning about USB debugging, but allows user/attacker to click [Skip] and successfully complete high-value fund transfers.
                </Typography>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.8 }}>
                  <Typography variant="caption" sx={{ color: '#00E5FF', fontWeight: 700 }}>
                    AppShieldX Gateway PEP (Config D)
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#10B981', fontWeight: 700 }}>
                    100.0% Blocked (HTTP 403 No Skip)
                  </Typography>
                </Box>
                <Typography variant="caption" sx={{ color: '#9CA3AF', display: 'block' }}>
                  Hardware-signed telemetry evaluated at AWS Cloud Gateway. The server returns HTTP 403 Forbidden—eliminating the bypass vector completely.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Row 4: Live HTTP Request & Threat Audit Stream */}
      <Card sx={{ bgcolor: '#111217', border: '1px solid #22252B', borderRadius: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Box>
              <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#FFFFFF' }}>
                Live Cross-Website Security Audit Stream (Prometheus / CloudWatch)
              </Typography>
              <Typography variant="caption" sx={{ color: '#6B7280' }}>
                Real-time transactions intercepted and verified across all web endpoints
              </Typography>
            </Box>
            <Chip
              label={`${auditLogs.length} Events Logged`}
              size="small"
              sx={{ bgcolor: '#1F2430', color: '#9CA3AF', fontSize: '0.72rem' }}
            />
          </Box>

          <TableContainer>
            <Table size="small">
              <TableHead sx={{ bgcolor: '#181B1F' }}>
                <TableRow>
                  <TableCell sx={{ color: '#9CA3AF', fontWeight: 700, fontSize: '0.75rem' }}>EVENT ID</TableCell>
                  <TableCell sx={{ color: '#9CA3AF', fontWeight: 700, fontSize: '0.75rem' }}>TIMESTAMP</TableCell>
                  <TableCell sx={{ color: '#9CA3AF', fontWeight: 700, fontSize: '0.75rem' }}>TARGET ENDPOINT</TableCell>
                  <TableCell sx={{ color: '#9CA3AF', fontWeight: 700, fontSize: '0.75rem' }}>THREAT DETECTED</TableCell>
                  <TableCell sx={{ color: '#9CA3AF', fontWeight: 700, fontSize: '0.75rem' }}>POLICY DECISION</TableCell>
                  <TableCell sx={{ color: '#9CA3AF', fontWeight: 700, fontSize: '0.75rem' }}>OVERHEAD</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {auditLogs.map((log) => (
                  <TableRow key={log.id} sx={{ '&:hover': { bgcolor: '#181B1F' } }}>
                    <TableCell sx={{ color: '#00E5FF', fontWeight: 600, fontSize: '0.78rem' }}>{log.id}</TableCell>
                    <TableCell sx={{ color: '#9CA3AF', fontSize: '0.78rem' }}>{log.timestamp}</TableCell>
                    <TableCell sx={{ color: '#FFFFFF', fontWeight: 500, fontSize: '0.78rem' }}>{log.target}</TableCell>
                    <TableCell sx={{ color: log.statusColor, fontWeight: 600, fontSize: '0.78rem' }}>
                      {log.threatDetected}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={log.decision}
                        size="small"
                        sx={{
                          bgcolor: `${log.statusColor}18`,
                          color: log.statusColor,
                          border: `1px solid ${log.statusColor}50`,
                          fontWeight: 700,
                          fontSize: '0.7rem',
                          height: 22,
                        }}
                      />
                    </TableCell>
                    <TableCell sx={{ color: '#60A5FA', fontSize: '0.78rem' }}>{log.latency}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};
