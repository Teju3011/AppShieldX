package com.framework.threat.dto;

import java.time.Instant;
import java.util.Map;

public record StandardErrorResponse(
        Instant timestamp,
        int status,
        String error,
        String message,
        String path,
        String correlationId,
        Map<String, String> validationErrors
) {
    public static StandardErrorResponse of(int status, String error, String message, String path, String correlationId) {
        return new StandardErrorResponse(Instant.now(), status, error, message, path, correlationId, null);
    }

    public static StandardErrorResponse of(int status, String error, String message, String path, String correlationId, Map<String, String> validationErrors) {
        return new StandardErrorResponse(Instant.now(), status, error, message, path, correlationId, validationErrors);
    }
}
