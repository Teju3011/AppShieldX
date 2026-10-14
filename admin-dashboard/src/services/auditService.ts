import api from './api';

export interface AuditLog {
  id: string;
  correlationId: string;
  serviceName: string;
  action: string;
  actorId: string | null;
  actorRole: string | null;
  clientIp: string | null;
  status: 'SUCCESS' | 'FAILURE' | 'BLOCKED';
  details: string | null;
  timestamp: string;
}

export interface AuditStats {
  totalLogsRecorded: number;
  successfulActions: number;
  failedActions: number;
  blockedSecurityThreats: number;
  actionDistribution: Record<string, number>;
}

export const auditService = {
  getRecentLogs: async (limit: number = 50): Promise<AuditLog[]> => {
    const response = await api.get<AuditLog[]>(`/audit/logs?limit=${limit}`);
    return response.data;
  },

  getLogsByCorrelationId: async (correlationId: string): Promise<AuditLog[]> => {
    const response = await api.get<AuditLog[]>(`/audit/logs/correlation/${correlationId}`);
    return response.data;
  },

  getAuditStats: async (): Promise<AuditStats> => {
    const response = await api.get<AuditStats>('/audit/stats');
    return response.data;
  },
};
