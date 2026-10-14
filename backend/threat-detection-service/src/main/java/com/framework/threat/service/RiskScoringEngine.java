package com.framework.threat.service;

import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.Instant;
import java.util.HashSet;
import java.util.Set;

@Component
public class RiskScoringEngine {

    private final PolicyConfigurationService policyConfig;

    public record RiskEvaluation(
            int score,
            String riskLevel,
            String responseBand,
            Set<String> riskContributors,
            String explanation
    ) {}

    public RiskScoringEngine(PolicyConfigurationService policyConfig) {
        this.policyConfig = policyConfig;
    }

    public RiskEvaluation calculateScore(
            int previousScore,
            Instant lastEvaluatedAt,
            CrossLayerCorrelationEngine.CorrelationResult correlationResult
    ) {
        // 1. Decay previous score based on elapsed time (half-life of 10 minutes)
        int decayedScore = applyDecay(previousScore, lastEvaluatedAt);

        // 2. Add bounded risk contribution from correlation engine
        int contribution = correlationResult.riskContribution();
        int rawScore = decayedScore + contribution;

        // 3. Normalized score clamped to [0, 100]
        int finalScore = Math.min(100, Math.max(0, rawScore));

        // 4. Map to 4 Response Bands
        String responseBand = mapToResponseBand(finalScore);
        String riskLevel = mapToRiskLevel(finalScore);

        Set<String> contributors = new HashSet<>();
        if (correlationResult.matchedConditions() != null) {
            contributors.addAll(correlationResult.matchedConditions());
        }
        if (correlationResult.correlationRuleId() != null) {
            contributors.add("RULE:" + correlationResult.correlationRuleId());
        }

        return new RiskEvaluation(
                finalScore,
                riskLevel,
                responseBand,
                contributors,
                correlationResult.explanation()
        );
    }

    public int applyDecay(int score, Instant lastEvaluatedAt) {
        if (score <= 0 || lastEvaluatedAt == null) return 0;
        long elapsedMinutes = Duration.between(lastEvaluatedAt, Instant.now()).toMinutes();
        if (elapsedMinutes <= 5) return score; // Fresh score within 5 minutes

        // 50% decay for every 10 minutes elapsed
        double decayFactor = Math.pow(0.5, (double) elapsedMinutes / 10.0);
        return (int) Math.round(score * decayFactor);
    }

    public String mapToResponseBand(int score) {
        int allowMax = policyConfig.getInt("risk.bands.allow_max", 24);
        int monitorMax = policyConfig.getInt("risk.bands.monitor_max", 49);
        int stepUpMax = policyConfig.getInt("risk.bands.step_up_max", 74);

        if (score <= allowMax) {
            return "ALLOW";
        } else if (score <= monitorMax) {
            return "MONITOR";
        } else if (score <= stepUpMax) {
            return "STEP_UP_AUTHENTICATION";
        } else {
            return "RESTRICT_SENSITIVE_ACTIONS";
        }
    }

    public String mapToRiskLevel(int score) {
        if (score >= 75) return "CRITICAL";
        if (score >= 50) return "HIGH";
        if (score >= 25) return "MEDIUM";
        return "LOW";
    }
}
