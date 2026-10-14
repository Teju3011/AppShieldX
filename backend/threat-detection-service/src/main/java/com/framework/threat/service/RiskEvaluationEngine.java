package com.framework.threat.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.*;

@Component
public class RiskEvaluationEngine {

    private final int rootWeight;
    private final int fridaWeight;
    private final int debuggerWeight;
    private final int integrityWeight;
    private final int emulatorWeight;
    private final int velocityBurstWeight;
    private final int velocityThreshold;

    public record EvaluationResult(int score, String riskLevel, Set<String> threatFlags) {}

    public RiskEvaluationEngine(
            @Value("${threat-detection.weights.root-jailbreak:40}") int rootWeight,
            @Value("${threat-detection.weights.frida-hook:50}") int fridaWeight,
            @Value("${threat-detection.weights.debugger:30}") int debuggerWeight,
            @Value("${threat-detection.weights.integrity:35}") int integrityWeight,
            @Value("${threat-detection.weights.emulator:15}") int emulatorWeight,
            @Value("${threat-detection.weights.velocity-burst:20}") int velocityBurstWeight,
            @Value("${threat-detection.velocity-threshold-per-minute:10}") int velocityThreshold
    ) {
        this.rootWeight = rootWeight;
        this.fridaWeight = fridaWeight;
        this.debuggerWeight = debuggerWeight;
        this.integrityWeight = integrityWeight;
        this.emulatorWeight = emulatorWeight;
        this.velocityBurstWeight = velocityBurstWeight;
        this.velocityThreshold = velocityThreshold;
    }

    public EvaluationResult evaluateRisk(Set<String> detectedThreats, long currentVelocity) {
        int score = 0;
        Set<String> activeFlags = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);

        if (detectedThreats != null) {
            for (String threat : detectedThreats) {
                String normalized = threat.trim().toUpperCase();
                if (normalized.contains("ROOT") || normalized.contains("JAILBREAK")) {
                    score += rootWeight;
                    activeFlags.add("ROOT_OR_JAILBREAK");
                } else if (normalized.contains("FRIDA") || normalized.contains("HOOK")) {
                    score += fridaWeight;
                    activeFlags.add("FRIDA_HOOK_INJECTION");
                } else if (normalized.contains("DEBUG")) {
                    score += debuggerWeight;
                    activeFlags.add("DEBUGGER_ATTACHED");
                } else if (normalized.contains("INTEGRITY") || normalized.contains("TAMPER")) {
                    score += integrityWeight;
                    activeFlags.add("SIGNATURE_TAMPERING");
                } else if (normalized.contains("EMULATOR") || normalized.contains("SIMULATOR")) {
                    score += emulatorWeight;
                    activeFlags.add("VIRTUAL_DEVICE");
                }
            }
        }

        if (currentVelocity >= velocityThreshold) {
            score += velocityBurstWeight;
            activeFlags.add("ANOMALOUS_EVENT_BURST");
        }

        int clampedScore = Math.min(100, Math.max(0, score));
        String level = mapScoreToLevel(clampedScore);

        return new EvaluationResult(clampedScore, level, activeFlags);
    }

    public String mapScoreToLevel(int score) {
        if (score >= 90) return "CRITICAL";
        if (score >= 70) return "HIGH";
        if (score >= 40) return "MEDIUM";
        return "LOW";
    }
}
