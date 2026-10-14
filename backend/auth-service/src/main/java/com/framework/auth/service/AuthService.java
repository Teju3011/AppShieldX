package com.framework.auth.service;

import com.framework.auth.dto.*;

/**
 * Service interface governing user registration, authentication, token rotation, and revocation.
 */
public interface AuthService {
    UserDto register(RegisterRequest request, String ipAddress, String correlationId);
    AuthResponse login(LoginRequest request, String ipAddress, String correlationId);
    TokenRefreshResponse refreshToken(TokenRefreshRequest request, String ipAddress, String correlationId);
    void logout(String authHeader, String ipAddress, String correlationId);
}
