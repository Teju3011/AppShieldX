package com.framework.audit.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.Instant;

public record CreateAuditLogRequest(
        String correlationId,

        @NotBlank(message = "ServiceName is required")
        @Size(max = 60, message = "ServiceName cannot exceed 60 characters")
        String serviceName,

        @NotBlank(message = "Action is required")
        @Size(max = 60, message = "Action cannot exceed 60 characters")
        String action,

        String actorId,

        String actorRole,

        String clientIp,

        @NotBlank(message = "Status is required")
        @Size(max = 20, message = "Status cannot exceed 20 characters")
        String status, // SUCCESS, FAILURE, BLOCKED

        String details,

        Instant timestamp
) {}
