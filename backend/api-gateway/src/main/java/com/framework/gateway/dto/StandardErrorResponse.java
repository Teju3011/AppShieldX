package com.framework.gateway.dto;

import java.time.Instant;

/**
 * Standardized RFC 7807 compliant error representation returned by API Gateway.
 */
public record StandardErrorResponse(
        String timestamp,
        int status,
        String error,
        String message,
        String path,
        String correlationId
) {
    public static StandardErrorResponse of(int status, String error, String message, String path, String correlationId) {
        return new StandardErrorResponse(
                Instant.now().toString(),
                status,
                error,
                message,
                path,
                correlationId != null ? correlationId : "N/A"
        );
    }
}
