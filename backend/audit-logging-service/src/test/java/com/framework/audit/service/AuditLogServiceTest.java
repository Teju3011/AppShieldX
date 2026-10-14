package com.framework.audit.service;

import com.framework.audit.dto.AuditLogResponse;
import com.framework.audit.dto.AuditStatsResponse;
import com.framework.audit.dto.CreateAuditLogRequest;
import com.framework.audit.entity.AuditLog;
import com.framework.audit.repository.AuditLogRepository;
import com.framework.audit.service.impl.AuditLogServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("AuditLogService Unit Tests")
class AuditLogServiceTest {

    @Mock
    private AuditLogRepository auditRepository;

    private AuditLogServiceImpl auditService;

    private static final String CORRELATION_ID = "corr-uuid-7788-9900";
    private AuditLog sampleLog;

    @BeforeEach
    void setUp() {
        auditService = new AuditLogServiceImpl(auditRepository);

        sampleLog = new AuditLog(
                CORRELATION_ID,
                "api-gateway",
                "AUTH_LOGIN",
                "user-uuid-1122",
                "ROLE_USER",
                "192.168.1.50",
                "SUCCESS",
                "Authentication passed via mobile device",
                Instant.now()
        );
        sampleLog.setId(UUID.randomUUID());
    }

    @Test
    @DisplayName("Should successfully record audit log with correlation ID")
    void testRecordLogSuccess() {
        CreateAuditLogRequest request = new CreateAuditLogRequest(
                CORRELATION_ID,
                "api-gateway",
                "AUTH_LOGIN",
                "user-uuid-1122",
                "ROLE_USER",
                "192.168.1.50",
                "SUCCESS",
                "Authentication passed",
                Instant.now()
        );

        when(auditRepository.save(any(AuditLog.class))).thenReturn(sampleLog);

        AuditLogResponse response = auditService.recordLog(request);

        assertNotNull(response);
        assertEquals(CORRELATION_ID, response.correlationId());
        assertEquals("api-gateway", response.serviceName());
        assertEquals("AUTH_LOGIN", response.action());
        assertEquals("SUCCESS", response.status());
        verify(auditRepository, times(1)).save(any(AuditLog.class));
    }

    @Test
    @DisplayName("Should query audit log timeline by correlation ID")
    void testGetLogsByCorrelationId() {
        when(auditRepository.findByCorrelationIdOrderByTimestampAsc(CORRELATION_ID))
                .thenReturn(List.of(sampleLog));

        List<AuditLogResponse> logs = auditService.getLogsByCorrelationId(CORRELATION_ID);

        assertNotNull(logs);
        assertEquals(1, logs.size());
        assertEquals(CORRELATION_ID, logs.get(0).correlationId());
        verify(auditRepository, times(1)).findByCorrelationIdOrderByTimestampAsc(CORRELATION_ID);
    }

    @Test
    @DisplayName("Should calculate SIEM audit metrics and statistics")
    void testGetAuditStats() {
        when(auditRepository.count()).thenReturn(200L);
        when(auditRepository.countByStatus("SUCCESS")).thenReturn(170L);
        when(auditRepository.countByStatus("FAILURE")).thenReturn(20L);
        when(auditRepository.countByStatus("BLOCKED")).thenReturn(10L);
        when(auditRepository.countGroupedByAction()).thenReturn(List.of(
                new Object[]{"AUTH_LOGIN", 120L},
                new Object[]{"RECORD_MUTATION", 80L}
        ));

        AuditStatsResponse stats = auditService.getAuditStats();

        assertNotNull(stats);
        assertEquals(200L, stats.totalLogsRecorded());
        assertEquals(170L, stats.successfulActions());
        assertEquals(20L, stats.failedActions());
        assertEquals(10L, stats.blockedSecurityThreats());
        assertEquals(120L, stats.actionDistribution().get("AUTH_LOGIN"));
    }
}
