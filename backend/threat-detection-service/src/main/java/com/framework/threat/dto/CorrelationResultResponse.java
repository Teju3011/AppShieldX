package com.framework.threat.dto;

import java.time.Instant;
import java.util.List;

public record CorrelationResultResponse(
        String correlationId,
        String correlationRuleId,
        List<String> matchedConditions,
        List<String> relatedEventReferences,
        int timeWindowSeconds,
        int riskScoreBefore,
        int riskScoreAfter,
        int riskContribution,
        String confidence,
        String explanation,
        String recommendedPolicyAction,
        String finalEnforcedAction,
        String platform,
        Instant timestamp
) {}
