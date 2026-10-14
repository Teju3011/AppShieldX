package com.framework.auth.dto;

import java.util.List;
import java.util.UUID;

/**
 * Public DTO representing user identity and role authorizations.
 */
public record UserDto(
        UUID id,
        String username,
        String email,
        List<String> roles
) {}
