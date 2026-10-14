package com.framework.threat.dto;

import java.util.Map;

public record ThreatSummaryResponse(
        long totalEventsRecorded,
        long criticalSeverityEvents,
        long highSeverityEvents,
        long highRiskDevicesActive,
        Map<String, Long> categoryDistribution
) {}
