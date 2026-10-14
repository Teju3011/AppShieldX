package com.framework.threat.service;

import com.framework.threat.dto.*;
import com.framework.threat.entity.CorrelationRecordEntity;
import com.framework.threat.entity.DeviceRiskProfile;
import com.framework.threat.entity.SecurityEventEntity;
import com.framework.threat.repository.CorrelationRecordRepository;
import com.framework.threat.repository.DeviceRiskProfileRepository;
import com.framework.threat.repository.PolicyConfigurationRepository;
import com.framework.threat.repository.SecurityEventRepository;
import com.framework.threat.service.impl.ThreatDetectionServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("ThreatDetectionService & Cross-Layer Correlation Unit Tests")
class ThreatDetectionServiceTest {

    @Mock
    private SecurityEventRepository eventRepository;

    @Mock
    private DeviceRiskProfileRepository deviceRiskRepository;

    @Mock
    private CorrelationRecordRepository correlationRepository;

    @Mock
    private PolicyConfigurationRepository policyConfigRepository;

    @Mock
    private ThreatCacheService threatCacheService;

    private EventValidationService validationService;
    private EventEnrichmentService enrichmentService;
    private PolicyConfigurationService policyConfigService;
    private CrossLayerCorrelationEngine correlationEngine;
    private RiskScoringEngine riskScoringEngine;
    private ExperimentMetricsTracker metricsTracker;
    private ThreatDetectionServiceImpl threatService;

    private static final String DEVICE_ID = "android-device-uuid-9988";

    @BeforeEach
    void setUp() {
        validationService = new EventValidationService();
        enrichmentService = new EventEnrichmentService();
        policyConfigService = new PolicyConfigurationService(policyConfigRepository);
        policyConfigService.init();

        correlationEngine = new CrossLayerCorrelationEngine(eventRepository, policyConfigService);
        riskScoringEngine = new RiskScoringEngine(policyConfigService);
        metricsTracker = new ExperimentMetricsTracker(policyConfigService);

        threatService = new ThreatDetectionServiceImpl(
                eventRepository,
                deviceRiskRepository,
                correlationRepository,
                threatCacheService,
                validationService,
                enrichmentService,
                correlationEngine,
                riskScoringEngine,
                policyConfigService,
                metricsTracker
        );
    }

    @Test
    @DisplayName("Should ingest security event and compute cross-layer risk profile")
    void testIngestEventSuccess() {
        SecurityEventRequest request = new SecurityEventRequest(
                DEVICE_ID,
                "ROOT_DETECTED",
                "HIGH",
                "MOBILE_INTEGRITY",
                "su binary detected in /system/bin/su",
                Instant.now()
        );

        SecurityEventEntity savedEntity = new SecurityEventEntity(
                DEVICE_ID,
                null,
                "ROOT_DETECTED",
                "HIGH",
                "MOBILE_INTEGRITY",
                "su binary detected",
                "192.168.1.100",
                Instant.now()
        );
        savedEntity.setId(UUID.randomUUID());
        savedEntity.setEventId(UUID.randomUUID().toString());

        when(eventRepository.save(any(SecurityEventEntity.class))).thenReturn(savedEntity);
        when(deviceRiskRepository.findById(DEVICE_ID)).thenReturn(Optional.empty());

        SecurityEventResponse response = threatService.ingestEvent(request, null, "192.168.1.100");

        assertNotNull(response);
        assertEquals(DEVICE_ID, response.deviceId());
        assertEquals("ROOT_DETECTED", response.eventType());
        verify(eventRepository, times(1)).save(any(SecurityEventEntity.class));
        verify(deviceRiskRepository, times(1)).save(any(DeviceRiskProfile.class));
        verify(correlationRepository, times(1)).save(any(CorrelationRecordEntity.class));
    }

    @Test
    @DisplayName("Should detect cross-layer threat when mobile RASP coincides with API auth failure")
    void testCrossLayerCorrelationRule01() {
        String sessionRef = "session-test-jwt-123";
        UUID userId = UUID.randomUUID();

        // 1. Prior mobile RASP event in repository
        SecurityEventEntity priorRasp = new SecurityEventEntity(
                DEVICE_ID,
                userId,
                "FRIDA_ATTACHED",
                "HIGH",
                "MOBILE_RASP",
                "Frida gadget injected",
                "192.168.1.100",
                Instant.now().minusSeconds(10)
        );
        priorRasp.setId(UUID.randomUUID());
        priorRasp.setEventId(UUID.randomUUID().toString());
        priorRasp.setVerifiedSessionRef(sessionRef);

        when(eventRepository.findCorrelatableEvents(any(), any(), any(), any()))
                .thenReturn(List.of(priorRasp));

        // 2. Incoming API auth denial on the same verified session
        CommonSecurityEventRequest apiEvent = new CommonSecurityEventRequest(
                UUID.randomUUID().toString(),
                Instant.now(),
                "API_GATEWAY",
                "1.0.0",
                "AUTHZ_DENIED",
                "HIGH",
                1.0,
                userId.toString(),
                sessionRef,
                DEVICE_ID,
                UUID.randomUUID().toString(),
                "AUTH_GATEWAY",
                "Unauthorized access to sensitive resource /api/records/admin",
                "GATEWAY_FILTER",
                "SERVER_VERIFIED",
                Instant.now().plus(Duration.ofMinutes(15)),
                "Access denied for user without required scope"
        );

        SecurityEventEntity savedApiEntity = new SecurityEventEntity();
        savedApiEntity.setId(UUID.randomUUID());
        savedApiEntity.setEventId(apiEvent.eventId());
        savedApiEntity.setDeviceId(DEVICE_ID);
        savedApiEntity.setEventType(apiEvent.eventType());
        savedApiEntity.setSeverity(apiEvent.severity());
        savedApiEntity.setPlatform(apiEvent.platform());
        savedApiEntity.setVerifiedSessionRef(sessionRef);
        savedApiEntity.setAuthUserRef(userId.toString());
        savedApiEntity.setTimestamp(Instant.now());

        when(eventRepository.save(any(SecurityEventEntity.class))).thenReturn(savedApiEntity);
        when(deviceRiskRepository.findById(DEVICE_ID)).thenReturn(Optional.empty());

        CorrelationResultResponse correlationResponse = threatService.ingestCommonEvent(apiEvent, userId, "192.168.1.100");

        assertNotNull(correlationResponse);
        assertEquals("RULE-CORR-01", correlationResponse.correlationRuleId());
        assertEquals("RESTRICT_SENSITIVE_ACTIONS", correlationResponse.finalEnforcedAction());
        assertTrue(correlationResponse.riskScoreAfter() >= 65);
        verify(correlationRepository, times(1)).save(any(CorrelationRecordEntity.class));
    }

    @Test
    @DisplayName("Should detect event replay and suppress risk escalation (RULE-CORR-04)")
    void testEventReplayDeduplication() {
        CommonSecurityEventRequest event = new CommonSecurityEventRequest(
                UUID.randomUUID().toString(),
                Instant.now(),
                "ANDROID",
                "1.0.0",
                "ROOT_DETECTED",
                "HIGH",
                1.0,
                null,
                "session-1",
                DEVICE_ID,
                UUID.randomUUID().toString(),
                "MOBILE_RASP",
                "su binary detected in system",
                "CLIENT_TELEMETRY",
                "UNVERIFIED_CLIENT",
                Instant.now().plus(Duration.ofMinutes(15)),
                "su check"
        );

        SecurityEventEntity priorEntity = new SecurityEventEntity();
        priorEntity.setId(UUID.randomUUID());
        priorEntity.setEventId("prior-event-id-1");
        priorEntity.setEventHash(validationService.computeEventHash(event));

        when(eventRepository.findFirstByEventHashAndTimestampAfter(anyString(), any()))
                .thenReturn(Optional.of(priorEntity));

        SecurityEventEntity currentSaved = new SecurityEventEntity();
        currentSaved.setId(UUID.randomUUID());
        currentSaved.setEventId(event.eventId());
        currentSaved.setDeviceId(DEVICE_ID);
        currentSaved.setEventHash(priorEntity.getEventHash());
        currentSaved.setEventType(event.eventType());
        currentSaved.setTimestamp(Instant.now());

        when(eventRepository.save(any(SecurityEventEntity.class))).thenReturn(currentSaved);
        when(deviceRiskRepository.findById(DEVICE_ID)).thenReturn(Optional.of(new DeviceRiskProfile(DEVICE_ID, 20, "LOW", "CLEAN")));

        CorrelationResultResponse response = threatService.ingestCommonEvent(event, null, "127.0.0.1");

        assertNotNull(response);
        assertEquals("RULE-CORR-04", response.correlationRuleId());
        assertEquals(0, response.riskContribution(), "Replay should contribute 0 additional risk");
    }

    @Test
    @DisplayName("Should retrieve device risk profile")
    void testGetDeviceRisk() {
        DeviceRiskProfile profile = new DeviceRiskProfile(DEVICE_ID, 50, "MEDIUM", "FRIDA_HOOK_INJECTION");
        when(deviceRiskRepository.findById(DEVICE_ID)).thenReturn(Optional.of(profile));

        DeviceRiskResponse response = threatService.getDeviceRisk(DEVICE_ID);

        assertNotNull(response);
        assertEquals(DEVICE_ID, response.deviceId());
        assertEquals(50, response.riskScore());
        assertEquals("MEDIUM", response.riskLevel());
        assertTrue(response.activeThreats().contains("FRIDA_HOOK_INJECTION"));
    }

    @Test
    @DisplayName("Should aggregate threat metrics summary")
    void testGetThreatSummary() {
        when(eventRepository.count()).thenReturn(150L);
        when(eventRepository.countBySeverity("CRITICAL")).thenReturn(12L);
        when(eventRepository.countBySeverity("HIGH")).thenReturn(28L);
        when(deviceRiskRepository.countByRiskScoreGreaterThanEqual(50)).thenReturn(5L);
        when(eventRepository.countGroupedByThreatCategory()).thenReturn(List.of(
                new Object[]{"MOBILE_INTEGRITY", 85L},
                new Object[]{"API_ABUSE", 65L}
        ));

        ThreatSummaryResponse summary = threatService.getThreatSummary();

        assertNotNull(summary);
        assertEquals(150L, summary.totalEventsRecorded());
        assertEquals(12L, summary.criticalSeverityEvents());
        assertEquals(28L, summary.highSeverityEvents());
        assertEquals(5L, summary.highRiskDevicesActive());
        assertEquals(85L, summary.categoryDistribution().get("MOBILE_INTEGRITY"));
    }
}
