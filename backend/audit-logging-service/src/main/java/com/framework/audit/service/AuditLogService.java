package com.framework.audit.service;

import com.framework.audit.dto.AuditLogResponse;
import com.framework.audit.dto.AuditStatsResponse;
import com.framework.audit.dto.CreateAuditLogRequest;

import java.util.List;

public interface AuditLogService {

    AuditLogResponse recordLog(CreateAuditLogRequest request);

    List<AuditLogResponse> getLogsByCorrelationId(String correlationId);

    List<AuditLogResponse> getRecentLogs(int limit);

    AuditStatsResponse getAuditStats();
}
