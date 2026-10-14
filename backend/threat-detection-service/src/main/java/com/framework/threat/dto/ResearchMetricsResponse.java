package com.framework.threat.dto;

import java.util.Map;

public record ResearchMetricsResponse(
        String configuration,
        long totalEvaluations,
        long truePositives,
        long falsePositives,
        long trueNegatives,
        long falseNegatives,
        double recall,
        double precision,
        double falsePositiveRate,
        double f1Score,
        double medianLatencyMs,
        double p95LatencyMs,
        double avgIngestionLatencyMs,
        double avgCorrelationLatencyMs,
        double avgEnforcementLatencyMs,
        Map<String, Long> ruleTriggerCounts,
        Map<String, Long> enforcedActionCounts
) {}
