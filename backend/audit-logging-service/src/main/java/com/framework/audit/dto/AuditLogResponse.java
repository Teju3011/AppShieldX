package com.framework.audit.dto;

import java.time.Instant;
import java.util.UUID;

public record AuditLogResponse(
        UUID id,
        String correlationId,
        String serviceName,
        String action,
        String actorId,
        String actorRole,
        String clientIp,
        String status,
        String details,
        Instant timestamp
) {}
