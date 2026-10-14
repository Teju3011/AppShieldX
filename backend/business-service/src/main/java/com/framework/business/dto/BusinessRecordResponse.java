package com.framework.business.dto;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

public record BusinessRecordResponse(
        UUID id,
        UUID userId,
        String title,
        String category,
        String sensitiveData,
        BigDecimal amount,
        String status,
        String riskLevel,
        Instant createdAt,
        Instant updatedAt
) {}
