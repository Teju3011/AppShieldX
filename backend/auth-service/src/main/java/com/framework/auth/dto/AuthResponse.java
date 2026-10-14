package com.framework.auth.dto;

/**
 * DTO returned upon successful user authentication.
 */
public record AuthResponse(
        String accessToken,
        String refreshToken,
        String tokenType,
        long expiresIn,
        UserDto user
) {
    public static AuthResponse of(String accessToken, String refreshToken, long expiresIn, UserDto user) {
        return new AuthResponse(accessToken, refreshToken, "Bearer", expiresIn, user);
    }
}
