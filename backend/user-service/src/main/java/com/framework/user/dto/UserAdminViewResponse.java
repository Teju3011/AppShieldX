package com.framework.user.dto;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

public record UserAdminViewResponse(
        UUID userId,
        String username,
        String email,
        List<String> roles,
        boolean enabled,
        boolean accountLocked,
        Instant createdAt,
        Instant updatedAt
) {}
