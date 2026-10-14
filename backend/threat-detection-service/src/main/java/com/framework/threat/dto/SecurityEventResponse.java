package com.framework.threat.dto;

import java.time.Instant;
import java.util.UUID;

public record SecurityEventResponse(
        UUID id,
        String deviceId,
        UUID userId,
        String eventType,
        String severity,
        String threatCategory,
        String details,
        String clientIp,
        Instant timestamp
) {}
