package com.framework.user.dto;

import jakarta.validation.constraints.NotNull;

public record UpdateUserStatusRequest(
        @NotNull(message = "Enabled flag must be specified")
        Boolean enabled,

        @NotNull(message = "AccountLocked flag must be specified")
        Boolean accountLocked
) {}
