package com.framework.threat.service;

import com.framework.threat.dto.ExperimentConfigDto;
import com.framework.threat.entity.SecurityEventEntity;
import com.framework.threat.repository.SecurityEventRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.Instant;
import java.util.*;

@Component
public class CrossLayerCorrelationEngine {

    private static final Logger log = LoggerFactory.getLogger(CrossLayerCorrelationEngine.class);

    private final SecurityEventRepository eventRepository;
    private final PolicyConfigurationService policyConfig;

    public record CorrelationResult(
            String correlationId,
            String correlationRuleId,
            List<String> matchedConditions,
            List<String> relatedEventReferences,
            int timeWindowSeconds,
            int riskContribution,
            String confidence,
            String explanation,
            String recommendedPolicyAction
    ) {}

    public CrossLayerCorrelationEngine(
            SecurityEventRepository eventRepository,
            PolicyConfigurationService policyConfig
    ) {
        this.eventRepository = eventRepository;
        this.policyConfig = policyConfig;
    }

    public CorrelationResult correlate(SecurityEventEntity currentEvent) {
        String correlationId = currentEvent.getCorrelationId() != null
                ? currentEvent.getCorrelationId()
                : UUID.randomUUID().toString();

        ExperimentConfigDto expConfig = policyConfig.getActiveExperimentConfig();
        String activeMode = expConfig.activeConfiguration();

        int windowSeconds = policyConfig.getInt("correlation.sliding_window_seconds", 300);
        int dedupTtlSeconds = policyConfig.getInt("correlation.dedup_ttl_seconds", 600);
        Instant windowStart = Instant.now().minus(Duration.ofSeconds(windowSeconds));
        Instant dedupStart = Instant.now().minus(Duration.ofSeconds(dedupTtlSeconds));

        // 1. DEDUPLICATION / REPLAY CHECK (RULE-CORR-04)
        if (currentEvent.getEventHash() != null) {
            Optional<SecurityEventEntity> duplicate = eventRepository.findFirstByEventHashAndTimestampAfter(
                    currentEvent.getEventHash(), dedupStart
            );
            // If another event with same hash exists and has different ID or prior timestamp
            if (duplicate.isPresent() && !duplicate.get().getId().equals(currentEvent.getId())) {
                log.info("CORRELATION_DEDUP: Event replay detected for hash {}. Suppressing score escalation.",
                        currentEvent.getEventHash());
                return new CorrelationResult(
                        correlationId,
                        "RULE-CORR-04",
                        List.of("EVENT_HASH_DUPLICATE", "REPLAY_WITHIN_DEDUP_WINDOW"),
                        List.of(duplicate.get().getEventId() != null ? duplicate.get().getEventId() : duplicate.get().getId().toString()),
                        dedupTtlSeconds,
                        0, // Bounded: 0 additional risk points
                        "HIGH",
                        "Event deduplication: Repeated or replayed security event detected within sliding window. Risk score escalation suppressed.",
                        "ALLOW"
                );
            }
        }

        // 2. CHECK EXPERIMENTAL CONFIGURATION
        if ("CONFIG_A_API_ONLY".equals(activeMode)) {
            // Mobile telemetry is ignored for correlation and risk decisions
            if ("ANDROID".equalsIgnoreCase(currentEvent.getPlatform()) || "IOS".equalsIgnoreCase(currentEvent.getPlatform())) {
                return new CorrelationResult(
                        correlationId,
                        "RULE-CONFIG-A-BYPASS",
                        List.of("CONFIG_A_API_ONLY_ACTIVE"),
                        List.of(currentEvent.getEventId()),
                        windowSeconds,
                        0,
                        "LOW",
                        "Experimental Configuration A (API-only): Mobile telemetry ignored for correlation decisions.",
                        "ALLOW"
                );
            }
            // For API events in Config A, return standard single-event evaluation without correlation
            return evaluateSingleEvent(currentEvent, correlationId, windowSeconds);
        }

        if ("CONFIG_B_MOBILE_ONLY".equals(activeMode)) {
            // Mobile telemetry collected for observation only; backend correlation disabled
            return new CorrelationResult(
                    correlationId,
                    "RULE-CONFIG-B-PASSIVE",
                    List.of("CONFIG_B_MOBILE_ONLY_ACTIVE"),
                    List.of(currentEvent.getEventId()),
                    windowSeconds,
                    0,
                    "MEDIUM",
                    "Experimental Configuration B (Mobile-only): Telemetry recorded for local observation; cross-layer correlation disabled.",
                    "ALLOW"
            );
        }

        if ("CONFIG_C_INDEPENDENT".equals(activeMode)) {
            // Independent evaluation only: single event scoring without cross-layer combinations
            return evaluateSingleEvent(currentEvent, correlationId, windowSeconds);
        }

        // 3. FULL APPSHIELDX CROSS-LAYER CORRELATION (CONFIG_D_FULL_APPSHIELDX)
        // Retrieve prior events within window matching device, session, or user
        List<SecurityEventEntity> relatedEvents = eventRepository.findCorrelatableEvents(
                currentEvent.getDeviceId(),
                currentEvent.getVerifiedSessionRef(),
                currentEvent.getAuthUserRef(),
                windowStart
        );

        List<String> relatedIds = new ArrayList<>();
        boolean hasMobileRasp = false;
        boolean hasApiAuthFailure = false;
        boolean hasGatewayRateLimit = false;
        int authzDenialCount = 0;

        for (SecurityEventEntity event : relatedEvents) {
            String eventIdStr = event.getEventId() != null ? event.getEventId() : event.getId().toString();
            relatedIds.add(eventIdStr);

            String type = event.getEventType() != null ? event.getEventType().toUpperCase() : "";
            String category = event.getThreatCategory() != null ? event.getThreatCategory().toUpperCase() : "";

            if (isRaspThreat(type, category)) {
                hasMobileRasp = true;
            }
            if (isAuthFailure(type)) {
                hasApiAuthFailure = true;
                if (type.contains("AUTHZ") || type.contains("FORBIDDEN") || type.contains("DENIED")) {
                    authzDenialCount++;
                }
            }
            if (isRateLimit(type, category)) {
                hasGatewayRateLimit = true;
            }
        }

        // Include current event in pattern assessment
        String currentType = currentEvent.getEventType().toUpperCase();
        String currentCat = currentEvent.getThreatCategory() != null ? currentEvent.getThreatCategory().toUpperCase() : "";
        if (isRaspThreat(currentType, currentCat)) {
            hasMobileRasp = true;
        }
        if (isAuthFailure(currentType)) {
            hasApiAuthFailure = true;
            if (currentType.contains("AUTHZ") || currentType.contains("FORBIDDEN") || currentType.contains("DENIED")) {
                authzDenialCount++;
            }
        }
        if (isRateLimit(currentType, currentCat)) {
            hasGatewayRateLimit = true;
        }

        // Check Benign runtime observation (Scenario 8)
        if (isBenignRuntimeObservation(currentEvent)) {
            return new CorrelationResult(
                    correlationId,
                    "RULE-CORR-05",
                    List.of("BENIGN_RUNTIME_INDICATOR", "LOW_RISK_CONFIDENCE"),
                    relatedIds,
                    windowSeconds,
                    5,
                    "LOW",
                    "Low-confidence or benign runtime observation. Legitimate user access preserved without disruption.",
                    "ALLOW"
            );
        }

        // RULE-CORR-01: Cross-layer Mobile RASP + API Auth Failure / Authorization Denial (Scenario 7)
        if (hasMobileRasp && hasApiAuthFailure) {
            int bonus = policyConfig.getInt("risk.weights.cross_layer_bonus", 25);
            int baseRasp = policyConfig.getInt("risk.weights.frida_hook", 50);
            int contribution = Math.min(100, baseRasp + bonus); // 50 + 25 = 75

            return new CorrelationResult(
                    correlationId,
                    "RULE-CORR-01",
                    List.of("MOBILE_RASP_INDICATOR", "API_AUTH_FAILURE_OBSERVED", "CROSS_LAYER_SESSION_MATCH"),
                    relatedIds,
                    windowSeconds,
                    contribution,
                    "HIGH",
                    "Cross-layer correlation detected runtime tampering indicators concurrent with backend API authorization/authentication failures on the same verified session.",
                    "RESTRICT_SENSITIVE_ACTIONS"
            );
        }

        // RULE-CORR-02: Cross-layer Mobile RASP + Gateway Rate-Limit Burst
        if (hasMobileRasp && hasGatewayRateLimit) {
            int bonus = policyConfig.getInt("risk.weights.cross_layer_bonus", 25);
            int contribution = Math.min(100, 50 + bonus); // 75

            return new CorrelationResult(
                    correlationId,
                    "RULE-CORR-02",
                    List.of("MOBILE_RASP_INDICATOR", "GATEWAY_RATE_LIMIT_BURST"),
                    relatedIds,
                    windowSeconds,
                    contribution,
                    "HIGH",
                    "Cross-layer correlation detected runtime tampering combined with repeated gateway rate-limit violations.",
                    "RESTRICT_SENSITIVE_ACTIONS"
            );
        }

        // RULE-CORR-03: Repeated Authorization Denial Burst (Scenario 4)
        if (authzDenialCount >= 2) {
            int authzWeight = policyConfig.getInt("risk.weights.authz_denial", 20);
            int contribution = Math.min(55, authzWeight * 2);

            return new CorrelationResult(
                    correlationId,
                    "RULE-CORR-03",
                    List.of("REPEATED_AUTHZ_DENIALS", "BURST_THRESHOLD_EXCEEDED"),
                    relatedIds,
                    windowSeconds,
                    contribution,
                    "HIGH",
                    "Repeated unauthorized access attempts against protected resources within sliding correlation window.",
                    "STEP_UP_AUTHENTICATION"
            );
        }

        // Fallback: evaluate single event
        return evaluateSingleEvent(currentEvent, correlationId, windowSeconds);
    }

    private CorrelationResult evaluateSingleEvent(SecurityEventEntity event, String correlationId, int windowSeconds) {
        String type = event.getEventType().toUpperCase();
        int contribution = 0;
        String action = "ALLOW";
        String explanation = "Standard single-layer security observation.";

        if (type.contains("ROOT") || type.contains("JAILBREAK")) {
            contribution = policyConfig.getInt("risk.weights.root_jailbreak", 40);
            action = "MONITOR";
            explanation = "Client reported root/jailbreak environment indicator.";
        } else if (type.contains("FRIDA") || type.contains("HOOK")) {
            contribution = policyConfig.getInt("risk.weights.frida_hook", 50);
            action = "STEP_UP_AUTHENTICATION";
            explanation = "Client reported runtime hook/instrumentation injection.";
        } else if (type.contains("DEBUG")) {
            contribution = policyConfig.getInt("risk.weights.debugger", 30);
            action = "MONITOR";
            explanation = "Client reported active debugger attachment.";
        } else if (type.contains("TAMPER") || type.contains("INTEGRITY")) {
            contribution = policyConfig.getInt("risk.weights.signature_tamper", 35);
            action = "MONITOR";
            explanation = "Package signature tampering or file integrity anomaly reported.";
        } else if (type.contains("EMULATOR") || type.contains("SIMULATOR")) {
            contribution = policyConfig.getInt("risk.weights.emulator", 15);
            action = "ALLOW";
            explanation = "Virtual device execution environment observed.";
        } else if (type.contains("AUTH_FAILURE") || type.contains("LOGIN_FAILED")) {
            contribution = policyConfig.getInt("risk.weights.auth_failure", 15);
            action = "MONITOR";
            explanation = "Authentication failure recorded.";
        } else if (type.contains("AUTHZ") || type.contains("FORBIDDEN")) {
            contribution = policyConfig.getInt("risk.weights.authz_denial", 20);
            action = "MONITOR";
            explanation = "Single authorization denial recorded.";
        } else if (type.contains("RATE_LIMIT")) {
            contribution = policyConfig.getInt("risk.weights.rate_limit_burst", 20);
            action = "MONITOR";
            explanation = "API rate-limit threshold exceeded.";
        }

        return new CorrelationResult(
                correlationId,
                "RULE-SINGLE-01",
                List.of("SINGLE_LAYER_EVALUATION", type),
                List.of(event.getEventId() != null ? event.getEventId() : event.getId().toString()),
                windowSeconds,
                contribution,
                "MEDIUM",
                explanation,
                action
        );
    }

    private boolean isRaspThreat(String type, String category) {
        return type.contains("ROOT") || type.contains("JAILBREAK") ||
                type.contains("FRIDA") || type.contains("HOOK") ||
                type.contains("DEBUG") || type.contains("TAMPER") ||
                type.contains("INTEGRITY") || category.contains("RASP");
    }

    private boolean isAuthFailure(String type) {
        return type.contains("AUTH_FAILURE") || type.contains("AUTHZ_DENIED") ||
                type.contains("LOGIN_FAILED") || type.contains("UNAUTHORIZED") ||
                type.contains("FORBIDDEN");
    }

    private boolean isRateLimit(String type, String category) {
        return type.contains("RATE_LIMIT") || type.contains("BURST") ||
                category.contains("RATE_LIMIT");
    }

    private boolean isBenignRuntimeObservation(SecurityEventEntity event) {
        Double confidence = event.getConfidence();
        String type = event.getEventType().toUpperCase();
        return (confidence != null && confidence < 0.6) ||
                type.contains("BENIGN") ||
                type.contains("DEVELOPER_OPTIONS") ||
                type.contains("DEV_MODE") ||
                type.contains("TEST_PROBE");
    }
}
