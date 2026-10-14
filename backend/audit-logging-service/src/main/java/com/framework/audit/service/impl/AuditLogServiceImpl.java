package com.framework.audit.service.impl;

import com.framework.audit.dto.AuditLogResponse;
import com.framework.audit.dto.AuditStatsResponse;
import com.framework.audit.dto.CreateAuditLogRequest;
import com.framework.audit.entity.AuditLog;
import com.framework.audit.repository.AuditLogRepository;
import com.framework.audit.service.AuditLogService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class AuditLogServiceImpl implements AuditLogService {

    private static final Logger log = LoggerFactory.getLogger(AuditLogServiceImpl.class);

    private final AuditLogRepository auditRepository;

    public AuditLogServiceImpl(AuditLogRepository auditRepository) {
        this.auditRepository = auditRepository;
    }

    @Override
    @Transactional
    public AuditLogResponse recordLog(CreateAuditLogRequest request) {
        String correlationId = request.correlationId();
        if (correlationId == null || correlationId.isBlank()) {
            correlationId = UUID.randomUUID().toString();
        }

        AuditLog entry = new AuditLog(
                correlationId,
                request.serviceName().trim(),
                request.action().trim().toUpperCase(),
                request.actorId(),
                request.actorRole(),
                request.clientIp(),
                request.status().trim().toUpperCase(),
                request.details(),
                request.timestamp() != null ? request.timestamp() : Instant.now()
        );

        AuditLog saved = auditRepository.save(entry);
        log.info("AUDIT_COMMITTED: [Service: {}, Action: {}, Status: {}, CorrID: {}]",
                saved.getServiceName(), saved.getAction(), saved.getStatus(), saved.getCorrelationId());

        return mapToResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public List<AuditLogResponse> getLogsByCorrelationId(String correlationId) {
        return auditRepository.findByCorrelationIdOrderByTimestampAsc(correlationId).stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public List<AuditLogResponse> getRecentLogs(int limit) {
        return auditRepository.findTop100ByOrderByTimestampDesc().stream()
                .limit(limit > 0 ? limit : 100)
                .map(this::mapToResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public AuditStatsResponse getAuditStats() {
        long total = auditRepository.count();
        long success = auditRepository.countByStatus("SUCCESS");
        long failed = auditRepository.countByStatus("FAILURE");
        long blocked = auditRepository.countByStatus("BLOCKED");

        Map<String, Long> actionDistribution = new HashMap<>();
        List<Object[]> grouped = auditRepository.countGroupedByAction();
        for (Object[] row : grouped) {
            String action = (String) row[0];
            Long count = (Long) row[1];
            actionDistribution.put(action, count);
        }

        return new AuditStatsResponse(total, success, failed, blocked, actionDistribution);
    }

    private AuditLogResponse mapToResponse(AuditLog entry) {
        return new AuditLogResponse(
                entry.getId(),
                entry.getCorrelationId(),
                entry.getServiceName(),
                entry.getAction(),
                entry.getActorId(),
                entry.getActorRole(),
                entry.getClientIp(),
                entry.getStatus(),
                entry.getDetails(),
                entry.getTimestamp()
        );
    }
}
