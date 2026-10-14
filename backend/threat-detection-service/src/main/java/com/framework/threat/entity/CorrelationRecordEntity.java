package com.framework.threat.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "correlation_records")
public class CorrelationRecordEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "correlation_id", nullable = false, unique = true, length = 100)
    private String correlationId;

    @Column(name = "correlation_rule_id", nullable = false, length = 60)
    private String correlationRuleId;

    @Column(name = "matched_conditions", nullable = false, columnDefinition = "TEXT")
    private String matchedConditions;

    @Column(name = "related_event_ids", nullable = false, columnDefinition = "TEXT")
    private String relatedEventIds;

    @Column(name = "time_window_seconds", nullable = false)
    private int timeWindowSeconds = 300;

    @Column(name = "risk_score_before", nullable = false)
    private int riskScoreBefore;

    @Column(name = "risk_score_after", nullable = false)
    private int riskScoreAfter;

    @Column(name = "risk_contribution", nullable = false)
    private int riskContribution;

    @Column(name = "confidence", nullable = false, length = 20)
    private String confidence = "HIGH";

    @Column(name = "explanation", nullable = false, columnDefinition = "TEXT")
    private String explanation;

    @Column(name = "recommended_policy_action", nullable = false, length = 40)
    private String recommendedPolicyAction;

    @Column(name = "final_enforced_action", nullable = false, length = 40)
    private String finalEnforcedAction;

    @Column(name = "user_reference", length = 100)
    private String userReference;

    @Column(name = "session_reference", length = 100)
    private String sessionReference;

    @Column(name = "device_reference", length = 100)
    private String deviceReference;

    @Column(name = "platform", length = 30)
    private String platform = "MULTI_LAYER";

    @Column(nullable = false)
    private Instant timestamp = Instant.now();

    public CorrelationRecordEntity() {}

    public CorrelationRecordEntity(
            String correlationId,
            String correlationRuleId,
            String matchedConditions,
            String relatedEventIds,
            int timeWindowSeconds,
            int riskScoreBefore,
            int riskScoreAfter,
            int riskContribution,
            String confidence,
            String explanation,
            String recommendedPolicyAction,
            String finalEnforcedAction,
            String userReference,
            String sessionReference,
            String deviceReference,
            String platform,
            Instant timestamp
    ) {
        this.correlationId = correlationId;
        this.correlationRuleId = correlationRuleId;
        this.matchedConditions = matchedConditions;
        this.relatedEventIds = relatedEventIds;
        this.timeWindowSeconds = timeWindowSeconds;
        this.riskScoreBefore = riskScoreBefore;
        this.riskScoreAfter = riskScoreAfter;
        this.riskContribution = riskContribution;
        this.confidence = confidence;
        this.explanation = explanation;
        this.recommendedPolicyAction = recommendedPolicyAction;
        this.finalEnforcedAction = finalEnforcedAction;
        this.userReference = userReference;
        this.sessionReference = sessionReference;
        this.deviceReference = deviceReference;
        this.platform = platform != null ? platform : "MULTI_LAYER";
        this.timestamp = timestamp != null ? timestamp : Instant.now();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    public void setCorrelationId(String correlationId) {
        this.correlationId = correlationId;
    }

    public String getCorrelationRuleId() {
        return correlationRuleId;
    }

    public void setCorrelationRuleId(String correlationRuleId) {
        this.correlationRuleId = correlationRuleId;
    }

    public String getMatchedConditions() {
        return matchedConditions;
    }

    public void setMatchedConditions(String matchedConditions) {
        this.matchedConditions = matchedConditions;
    }

    public String getRelatedEventIds() {
        return relatedEventIds;
    }

    public void setRelatedEventIds(String relatedEventIds) {
        this.relatedEventIds = relatedEventIds;
    }

    public int getTimeWindowSeconds() {
        return timeWindowSeconds;
    }

    public void setTimeWindowSeconds(int timeWindowSeconds) {
        this.timeWindowSeconds = timeWindowSeconds;
    }

    public int getRiskScoreBefore() {
        return riskScoreBefore;
    }

    public void setRiskScoreBefore(int riskScoreBefore) {
        this.riskScoreBefore = riskScoreBefore;
    }

    public int getRiskScoreAfter() {
        return riskScoreAfter;
    }

    public void setRiskScoreAfter(int riskScoreAfter) {
        this.riskScoreAfter = riskScoreAfter;
    }

    public int getRiskContribution() {
        return riskContribution;
    }

    public void setRiskContribution(int riskContribution) {
        this.riskContribution = riskContribution;
    }

    public String getConfidence() {
        return confidence;
    }

    public void setConfidence(String confidence) {
        this.confidence = confidence;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public String getRecommendedPolicyAction() {
        return recommendedPolicyAction;
    }

    public void setRecommendedPolicyAction(String recommendedPolicyAction) {
        this.recommendedPolicyAction = recommendedPolicyAction;
    }

    public String getFinalEnforcedAction() {
        return finalEnforcedAction;
    }

    public void setFinalEnforcedAction(String finalEnforcedAction) {
        this.finalEnforcedAction = finalEnforcedAction;
    }

    public String getUserReference() {
        return userReference;
    }

    public void setUserReference(String userReference) {
        this.userReference = userReference;
    }

    public String getSessionReference() {
        return sessionReference;
    }

    public void setSessionReference(String sessionReference) {
        this.sessionReference = sessionReference;
    }

    public String getDeviceReference() {
        return deviceReference;
    }

    public void setDeviceReference(String deviceReference) {
        this.deviceReference = deviceReference;
    }

    public String getPlatform() {
        return platform;
    }

    public void setPlatform(String platform) {
        this.platform = platform;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }
}
