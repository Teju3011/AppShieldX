import api from './api';

export interface SecurityEvent {
  id: string;
  deviceId: string;
  userId: string | null;
  eventType: string;
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  threatCategory: string;
  details: string;
  clientIp: string;
  timestamp: string;
  platform?: string;
  verifiedSessionRef?: string;
  confidence?: number;
  verificationStatus?: string;
}

export interface DeviceRiskProfile {
  deviceId: string;
  riskScore: number;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  activeThreats: string[];
  totalEventsRecorded: number;
  lastEvaluatedAt: string;
}

export interface ThreatSummary {
  totalEventsRecorded: number;
  criticalSeverityEvents: number;
  highSeverityEvents: number;
  highRiskDevicesActive: number;
  categoryDistribution: Record<string, number>;
}

export interface CorrelationResult {
  correlationId: string;
  correlationRuleId: string;
  matchedConditions: string[];
  relatedEventReferences: string[];
  timeWindowSeconds: number;
  riskScoreBefore: number;
  riskScoreAfter: number;
  riskContribution: number;
  confidence: string;
  explanation: string;
  recommendedPolicyAction: string;
  finalEnforcedAction: string;
  platform: string;
  timestamp: string;
}

export interface ExperimentConfig {
  activeConfiguration: string;
  description: string;
  correlationEnabled: boolean;
  adaptiveEnforcementEnabled: boolean;
  mobileTelemetryIngested: boolean;
}

export interface ResearchMetrics {
  configuration: string;
  totalEvaluations: number;
  truePositives: number;
  falsePositives: number;
  trueNegatives: number;
  falseNegatives: number;
  recall: number;
  precision: number;
  falsePositiveRate: number;
  f1Score: number;
  medianLatencyMs: number;
  p95LatencyMs: number;
  avgIngestionLatencyMs: number;
  avgCorrelationLatencyMs: number;
  avgEnforcementLatencyMs: number;
  ruleTriggerCounts: Record<string, number>;
  enforcedActionCounts: Record<string, number>;
}

export const threatService = {
  getThreatSummary: async (): Promise<ThreatSummary> => {
    const response = await api.get<ThreatSummary>('/security/threats/summary');
    return response.data;
  },

  getRecentEvents: async (limit: number = 50): Promise<SecurityEvent[]> => {
    const response = await api.get<SecurityEvent[]>(`/security/events?limit=${limit}`);
    return response.data;
  },

  getDeviceRisk: async (deviceId: string): Promise<DeviceRiskProfile> => {
    const response = await api.get<DeviceRiskProfile>(`/security/devices/${deviceId}/risk`);
    return response.data;
  },

  getCorrelations: async (limit: number = 50): Promise<CorrelationResult[]> => {
    const response = await api.get<CorrelationResult[]>(`/security/correlations?limit=${limit}`);
    return response.data;
  },

  getCorrelationById: async (id: string): Promise<CorrelationResult> => {
    const response = await api.get<CorrelationResult>(`/security/correlations/${id}`);
    return response.data;
  },

  getPolicyConfigurations: async (): Promise<Record<string, string>> => {
    const response = await api.get<Record<string, string>>('/security/policies');
    return response.data;
  },

  updatePolicyConfigurations: async (configs: Record<string, string>): Promise<Record<string, string>> => {
    const response = await api.put<Record<string, string>>('/security/policies', configs);
    return response.data;
  },

  getExperimentConfig: async (): Promise<ExperimentConfig> => {
    const response = await api.get<ExperimentConfig>('/security/experiments/config');
    return response.data;
  },

  setExperimentConfig: async (mode: string): Promise<ExperimentConfig> => {
    const response = await api.post<ExperimentConfig>('/security/experiments/config', { mode });
    return response.data;
  },

  getExperimentMetrics: async (): Promise<ResearchMetrics> => {
    const response = await api.get<ResearchMetrics>('/security/experiments/metrics');
    return response.data;
  },

  resetExperimentMetrics: async (): Promise<{ status: string; message: string }> => {
    const response = await api.post<{ status: string; message: string }>('/security/experiments/reset');
    return response.data;
  },
};
