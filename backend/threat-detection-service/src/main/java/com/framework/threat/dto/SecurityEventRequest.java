package com.framework.threat.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.Instant;

public record SecurityEventRequest(
        @NotBlank(message = "DeviceId is required")
        @Size(max = 100, message = "DeviceId cannot exceed 100 characters")
        String deviceId,

        @NotBlank(message = "EventType is required")
        @Size(max = 60, message = "EventType cannot exceed 60 characters")
        String eventType,

        @NotBlank(message = "Severity is required")
        @Size(max = 20, message = "Severity cannot exceed 20 characters")
        String severity, // INFO, LOW, MEDIUM, HIGH, CRITICAL

        @NotBlank(message = "ThreatCategory is required")
        @Size(max = 60, message = "ThreatCategory cannot exceed 60 characters")
        String threatCategory,

        String details,

        Instant timestamp
) {}
