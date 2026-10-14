package com.framework.threat.service.impl;

import com.framework.threat.dto.*;
import com.framework.threat.entity.CorrelationRecordEntity;
import com.framework.threat.entity.DeviceRiskProfile;
import com.framework.threat.entity.SecurityEventEntity;
import com.framework.threat.repository.CorrelationRecordRepository;
import com.framework.threat.repository.DeviceRiskProfileRepository;
import com.framework.threat.repository.SecurityEventRepository;
import com.framework.threat.service.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class ThreatDetectionServiceImpl implements ThreatDetectionService {

    private static final Logger log = LoggerFactory.getLogger(ThreatDetectionServiceImpl.class);

    private final SecurityEventRepository eventRepository;
    private final DeviceRiskProfileRepository deviceRiskRepository;
    private final CorrelationRecordRepository correlationRepository;
    private final ThreatCacheService threatCacheService;
    private final EventValidationService validationService;
    private final EventEnrichmentService enrichmentService;
    private final CrossLayerCorrelationEngine correlationEngine;
    private final RiskScoringEngine riskScoringEngine;
    private final PolicyConfigurationService policyConfigService;
    private final ExperimentMetricsTracker metricsTracker;

    public ThreatDetectionServiceImpl(
            SecurityEventRepository eventRepository,
            DeviceRiskProfileRepository deviceRiskRepository,
            CorrelationRecordRepository correlationRepository,
            ThreatCacheService threatCacheService,
            EventValidationService validationService,
            EventEnrichmentService enrichmentService,
            CrossLayerCorrelationEngine correlationEngine,
            RiskScoringEngine riskScoringEngine,
            PolicyConfigurationService policyConfigService,
            ExperimentMetricsTracker metricsTracker
    ) {
        this.eventRepository = eventRepository;
        this.deviceRiskRepository = deviceRiskRepository;
        this.correlationRepository = correlationRepository;
        this.threatCacheService = threatCacheService;
        this.validationService = validationService;
        this.enrichmentService = enrichmentService;
        this.correlationEngine = correlationEngine;
        this.riskScoringEngine = riskScoringEngine;
        this.policyConfigService = policyConfigService;
        this.metricsTracker = metricsTracker;
    }

    @Override
    @Transactional
    public SecurityEventResponse ingestEvent(SecurityEventRequest request, UUID userId, String clientIp) {
        CommonSecurityEventRequest commonRequest = new CommonSecurityEventRequest(
                UUID.randomUUID().toString(),
                request.timestamp() != null ? request.timestamp() : Instant.now(),
                "ANDROID",
                "1.0.0",
                request.eventType(),
                request.severity(),
                1.0,
                userId != null ? userId.toString() : null,
                null,
                request.deviceId(),
                UUID.randomUUID().toString(),
                request.threatCategory(),
                request.eventType(),
                "CLIENT_TELEMETRY",
                "UNVERIFIED_CLIENT",
                Instant.now().plus(Duration.ofMinutes(15)),
                request.details()
        );

        CorrelationResultResponse corrResult = ingestCommonEvent(commonRequest, userId, clientIp);

        // Map back to SecurityEventResponse
        return new SecurityEventResponse(
                UUID.fromString(corrResult.correlationId()),
                request.deviceId(),
                userId,
                request.eventType(),
                request.severity(),
                request.threatCategory(),
                request.details(),
                clientIp,
                request.timestamp() != null ? request.timestamp() : Instant.now()
        );
    }

    @Override
    @Transactional
    public CorrelationResultResponse ingestCommonEvent(CommonSecurityEventRequest request, UUID userId, String clientIp) {
        long t0 = System.nanoTime();

        // 1. COLLECT & VALIDATE
        EventValidationService.ValidationResult validation = validationService.validate(request);
        if (!validation.isValid()) {
            throw new IllegalArgumentException("Event validation failed: " + validation.rejectionReason());
        }
        double ingestionMs = (System.nanoTime() - t0) / 1_000_000.0;

        // 2. ENRICH
        SecurityEventEntity enriched = enrichmentService.enrich(request, userId, clientIp, validation.eventHash());
        SecurityEventEntity savedEvent = eventRepository.save(enriched);

        String deviceId = enriched.getDeviceId();
        threatCacheService.incrementDeviceVelocity(deviceId, Duration.ofMinutes(1));

        // 3. CORRELATE
        long tCorr0 = System.nanoTime();
        CrossLayerCorrelationEngine.CorrelationResult corrResult = correlationEngine.correlate(savedEvent);
        double correlationMs = (System.nanoTime() - tCorr0) / 1_000_000.0;

        // 4. SCORE
        DeviceRiskProfile profile = deviceRiskRepository.findById(deviceId)
                .orElseGet(() -> new DeviceRiskProfile(deviceId, 0, "LOW", "CLEAN"));

        int previousScore = profile.getRiskScore();
        Instant lastEvaluatedAt = profile.getLastEvaluatedAt();

        RiskScoringEngine.RiskEvaluation eval = riskScoringEngine.calculateScore(
                previousScore, lastEvaluatedAt, corrResult
        );

        // 5. ENFORCE
        long tEnf0 = System.nanoTime();
        String finalAction = eval.responseBand();
        double enforcementMs = (System.nanoTime() - tEnf0) / 1_000_000.0;

        // Update profile
        profile.setRiskScore(eval.score());
        profile.setRiskLevel(eval.riskLevel());
        profile.setActiveThreats(String.join(",", eval.riskContributors()));
        profile.setTotalEventsRecorded(profile.getTotalEventsRecorded() + 1);
        profile.setLastEvaluatedAt(Instant.now());
        deviceRiskRepository.save(profile);

        // Cache evaluated risk score in Redis
        threatCacheService.cacheRiskScore(deviceId, eval.score(), Duration.ofMinutes(15));

        // 6. AUDIT (Persist correlation record)
        CorrelationRecordEntity record = new CorrelationRecordEntity(
                corrResult.correlationId(),
                corrResult.correlationRuleId(),
                String.join(";", corrResult.matchedConditions()),
                String.join(";", corrResult.relatedEventReferences()),
                corrResult.timeWindowSeconds(),
                previousScore,
                eval.score(),
                corrResult.riskContribution(),
                corrResult.confidence(),
                eval.explanation(),
                corrResult.recommendedPolicyAction(),
                finalAction,
                enriched.getAuthUserRef(),
                enriched.getVerifiedSessionRef(),
                deviceId,
                enriched.getPlatform(),
                Instant.now()
        );
        correlationRepository.save(record);

        // 7. RECORD METRICS FOR RESEARCH EVALUATION
        boolean isAttack = !corrResult.correlationRuleId().contains("BENIGN") &&
                !corrResult.correlationRuleId().contains("REPLAY") &&
                corrResult.riskContribution() > 0;
        metricsTracker.recordEvaluation(
                isAttack,
                finalAction,
                corrResult.correlationRuleId(),
                ingestionMs,
                correlationMs,
                enforcementMs
        );

        log.info("CROSS_LAYER_CORRELATION: Rule={} [PreScore: {}, PostScore: {}, Action: {}, Device: {}, Session: {}]",
                corrResult.correlationRuleId(), previousScore, eval.score(), finalAction, deviceId, enriched.getVerifiedSessionRef());

        // 8. DISPLAY (Return response)
        return new CorrelationResultResponse(
                corrResult.correlationId(),
                corrResult.correlationRuleId(),
                corrResult.matchedConditions(),
                corrResult.relatedEventReferences(),
                corrResult.timeWindowSeconds(),
                previousScore,
                eval.score(),
                corrResult.riskContribution(),
                corrResult.confidence(),
                eval.explanation(),
                corrResult.recommendedPolicyAction(),
                finalAction,
                enriched.getPlatform(),
                record.getTimestamp()
        );
    }

    @Override
    @Transactional(readOnly = true)
    public DeviceRiskResponse getDeviceRisk(String deviceId) {
        DeviceRiskProfile profile = deviceRiskRepository.findById(deviceId)
                .orElseGet(() -> new DeviceRiskProfile(deviceId, 0, "LOW", "CLEAN"));

        List<String> threats = profile.getActiveThreats() != null && !profile.getActiveThreats().isBlank()
                ? Arrays.asList(profile.getActiveThreats().split(","))
                : Collections.emptyList();

        return new DeviceRiskResponse(
                profile.getDeviceId(),
                profile.getRiskScore(),
                profile.getRiskLevel(),
                threats,
                profile.getTotalEventsRecorded(),
                profile.getLastEvaluatedAt()
        );
    }

    @Override
    @Transactional(readOnly = true)
    public ThreatSummaryResponse getThreatSummary() {
        long total = eventRepository.count();
        long critical = eventRepository.countBySeverity("CRITICAL");
        long high = eventRepository.countBySeverity("HIGH");
        long highRiskDevices = deviceRiskRepository.countByRiskScoreGreaterThanEqual(50);

        Map<String, Long> categoryDistribution = new HashMap<>();
        List<Object[]> grouped = eventRepository.countGroupedByThreatCategory();
        for (Object[] row : grouped) {
            String category = (String) row[0];
            Long count = (Long) row[1];
            categoryDistribution.put(category, count);
        }

        return new ThreatSummaryResponse(
                total,
                critical,
                high,
                highRiskDevices,
                categoryDistribution
        );
    }

    @Override
    @Transactional(readOnly = true)
    public List<SecurityEventResponse> getRecentEvents(int limit) {
        return eventRepository.findTop50ByOrderByTimestampDesc().stream()
                .limit(limit > 0 ? limit : 50)
                .map(this::mapToEventResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public List<CorrelationResultResponse> getRecentCorrelations(int limit) {
        return correlationRepository.findTop50ByOrderByTimestampDesc().stream()
                .limit(limit > 0 ? limit : 50)
                .map(this::mapToCorrelationResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public CorrelationResultResponse getCorrelationById(String correlationId) {
        CorrelationRecordEntity entity = correlationRepository.findByCorrelationId(correlationId)
                .orElseThrow(() -> new NoSuchElementException("Correlation record not found: " + correlationId));
        return mapToCorrelationResponse(entity);
    }

    @Override
    public ExperimentConfigDto getActiveExperimentConfig() {
        return policyConfigService.getActiveExperimentConfig();
    }

    @Override
    @Transactional
    public void setActiveExperimentConfig(String configMode, String updatedBy) {
        policyConfigService.setActiveExperimentConfig(configMode, updatedBy);
    }

    @Override
    public ResearchMetricsResponse getExperimentMetrics() {
        return metricsTracker.getMetrics();
    }

    @Override
    public void resetExperimentMetrics() {
        metricsTracker.reset();
    }

    @Override
    public Map<String, String> getPolicyConfigurations() {
        return policyConfigService.getAllConfigurations();
    }

    @Override
    @Transactional
    public void updatePolicyConfigurations(Map<String, String> configs, String updatedBy) {
        policyConfigService.updateConfigurations(configs, updatedBy);
    }

    private SecurityEventResponse mapToEventResponse(SecurityEventEntity entity) {
        return new SecurityEventResponse(
                entity.getId(),
                entity.getDeviceId(),
                entity.getUserId(),
                entity.getEventType(),
                entity.getSeverity(),
                entity.getThreatCategory(),
                entity.getDetails(),
                entity.getClientIp(),
                entity.getTimestamp()
        );
    }

    private CorrelationResultResponse mapToCorrelationResponse(CorrelationRecordEntity r) {
        List<String> conditions = r.getMatchedConditions() != null && !r.getMatchedConditions().isBlank()
                ? Arrays.asList(r.getMatchedConditions().split(";"))
                : Collections.emptyList();

        List<String> relatedIds = r.getRelatedEventIds() != null && !r.getRelatedEventIds().isBlank()
                ? Arrays.asList(r.getRelatedEventIds().split(";"))
                : Collections.emptyList();

        return new CorrelationResultResponse(
                r.getCorrelationId(),
                r.getCorrelationRuleId(),
                conditions,
                relatedIds,
                r.getTimeWindowSeconds(),
                r.getRiskScoreBefore(),
                r.getRiskScoreAfter(),
                r.getRiskContribution(),
                r.getConfidence(),
                r.getExplanation(),
                r.getRecommendedPolicyAction(),
                r.getFinalEnforcedAction(),
                r.getPlatform(),
                r.getTimestamp()
        );
    }
}
