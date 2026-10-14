package com.framework.user.dto;

import jakarta.validation.constraints.NotEmpty;
import java.util.Set;

public record UpdateUserRolesRequest(
        @NotEmpty(message = "Roles set cannot be empty")
        Set<String> roles
) {}
