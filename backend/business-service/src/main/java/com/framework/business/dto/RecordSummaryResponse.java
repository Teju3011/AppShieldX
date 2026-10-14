package com.framework.business.dto;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

public record RecordSummaryResponse(
        UUID id,
        String title,
        String category,
        BigDecimal amount,
        String status,
        String riskLevel,
        Instant createdAt
) {}
