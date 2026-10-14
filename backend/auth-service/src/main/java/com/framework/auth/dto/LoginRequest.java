package com.framework.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/**
 * DTO for authentication login requests.
 */
public record LoginRequest(
        @NotBlank(message = "Email cannot be blank")
        @Email(message = "Email must be a valid email address")
        String email,

        @NotBlank(message = "Password cannot be blank")
        String password
) {}
