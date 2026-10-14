package com.framework.threat.dto;

import java.time.Instant;
import java.util.List;

public record DeviceRiskResponse(
        String deviceId,
        int riskScore,
        String riskLevel,
        List<String> activeThreats,
        long totalEventsRecorded,
        Instant lastEvaluatedAt
) {}
