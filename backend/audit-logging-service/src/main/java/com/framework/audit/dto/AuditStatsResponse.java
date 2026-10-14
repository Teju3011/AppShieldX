package com.framework.audit.dto;

import java.util.Map;

public record AuditStatsResponse(
        long totalLogsRecorded,
        long successfulActions,
        long failedActions,
        long blockedSecurityThreats,
        Map<String, Long> actionDistribution
) {}
