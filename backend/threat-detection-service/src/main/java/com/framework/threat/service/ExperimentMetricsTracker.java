package com.framework.threat.service;

import com.framework.threat.dto.ResearchMetricsResponse;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class ExperimentMetricsTracker {

    private final PolicyConfigurationService policyConfig;

    private final AtomicLong truePositives = new AtomicLong(0);
    private final AtomicLong falsePositives = new AtomicLong(0);
    private final AtomicLong trueNegatives = new AtomicLong(0);
    private final AtomicLong falseNegatives = new AtomicLong(0);
    private final AtomicLong totalEvaluations = new AtomicLong(0);

    private final List<Double> latenciesMs = Collections.synchronizedList(new ArrayList<>());
    private final List<Double> ingestionLatenciesMs = Collections.synchronizedList(new ArrayList<>());
    private final List<Double> correlationLatenciesMs = Collections.synchronizedList(new ArrayList<>());
    private final List<Double> enforcementLatenciesMs = Collections.synchronizedList(new ArrayList<>());

    private final Map<String, AtomicLong> ruleCounts = new ConcurrentHashMap<>();
    private final Map<String, AtomicLong> actionCounts = new ConcurrentHashMap<>();

    public ExperimentMetricsTracker(PolicyConfigurationService policyConfig) {
        this.policyConfig = policyConfig;
    }

    public void recordEvaluation(
            boolean isGroundTruthAttack,
            String detectedAction,
            String ruleId,
            double ingestionMs,
            double correlationMs,
            double enforcementMs
    ) {
        totalEvaluations.incrementAndGet();
        double totalLatency = ingestionMs + correlationMs + enforcementMs;

        latenciesMs.add(totalLatency);
        ingestionLatenciesMs.add(ingestionMs);
        correlationLatenciesMs.add(correlationMs);
        enforcementLatenciesMs.add(enforcementMs);

        ruleCounts.computeIfAbsent(ruleId != null ? ruleId : "UNKNOWN", k -> new AtomicLong(0)).incrementAndGet();
        actionCounts.computeIfAbsent(detectedAction != null ? detectedAction : "ALLOW", k -> new AtomicLong(0)).incrementAndGet();

        boolean isRestrictedOrStepUp = "RESTRICT_SENSITIVE_ACTIONS".equalsIgnoreCase(detectedAction) ||
                "STEP_UP_AUTHENTICATION".equalsIgnoreCase(detectedAction);

        if (isGroundTruthAttack) {
            if (isRestrictedOrStepUp) {
                truePositives.incrementAndGet();
            } else {
                falseNegatives.incrementAndGet();
            }
        } else {
            if (isRestrictedOrStepUp) {
                falsePositives.incrementAndGet();
            } else {
                trueNegatives.incrementAndGet();
            }
        }
    }

    public void reset() {
        truePositives.set(0);
        falsePositives.set(0);
        trueNegatives.set(0);
        falseNegatives.set(0);
        totalEvaluations.set(0);
        latenciesMs.clear();
        ingestionLatenciesMs.clear();
        correlationLatenciesMs.clear();
        enforcementLatenciesMs.clear();
        ruleCounts.clear();
        actionCounts.clear();
    }

    public ResearchMetricsResponse getMetrics() {
        long tp = truePositives.get();
        long fp = falsePositives.get();
        long tn = trueNegatives.get();
        long fn = falseNegatives.get();
        long total = totalEvaluations.get();

        double recall = (tp + fn) > 0 ? (double) tp / (tp + fn) : 0.0;
        double precision = (tp + fp) > 0 ? (double) tp / (tp + fp) : 0.0;
        double fpr = (fp + tn) > 0 ? (double) fp / (fp + tn) : 0.0;
        double f1 = (precision + recall) > 0 ? (2.0 * precision * recall) / (precision + recall) : 0.0;

        List<Double> sortedLatencies;
        synchronized (latenciesMs) {
            sortedLatencies = new ArrayList<>(latenciesMs);
        }
        Collections.sort(sortedLatencies);

        double medianLatency = 0.0;
        double p95Latency = 0.0;
        if (!sortedLatencies.isEmpty()) {
            medianLatency = sortedLatencies.get(sortedLatencies.size() / 2);
            int p95Index = (int) Math.min(sortedLatencies.size() - 1, Math.round(sortedLatencies.size() * 0.95));
            p95Latency = sortedLatencies.get(p95Index);
        }

        double avgIngestion = computeAvg(ingestionLatenciesMs);
        double avgCorrelation = computeAvg(correlationLatenciesMs);
        double avgEnforcement = computeAvg(enforcementLatenciesMs);

        Map<String, Long> rulesMap = new HashMap<>();
        for (var entry : ruleCounts.entrySet()) {
            rulesMap.put(entry.getKey(), entry.getValue().get());
        }

        Map<String, Long> actionsMap = new HashMap<>();
        for (var entry : actionCounts.entrySet()) {
            actionsMap.put(entry.getKey(), entry.getValue().get());
        }

        String activeConfig = policyConfig.getActiveExperimentConfig().activeConfiguration();

        return new ResearchMetricsResponse(
                activeConfig,
                total,
                tp,
                fp,
                tn,
                fn,
                recall,
                precision,
                fpr,
                f1,
                medianLatency,
                p95Latency,
                avgIngestion,
                avgCorrelation,
                avgEnforcement,
                rulesMap,
                actionsMap
        );
    }

    private double computeAvg(List<Double> list) {
        synchronized (list) {
            if (list.isEmpty()) return 0.0;
            double sum = 0.0;
            for (double d : list) sum += d;
            return sum / list.size();
        }
    }
}
