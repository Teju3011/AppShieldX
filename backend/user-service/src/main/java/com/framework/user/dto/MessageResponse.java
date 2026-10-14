package com.framework.user.dto;

import java.time.Instant;

public record MessageResponse(
        String message,
        Instant timestamp,
        String correlationId
) {
    public static MessageResponse of(String message, String correlationId) {
        return new MessageResponse(message, Instant.now(), correlationId);
    }
}
