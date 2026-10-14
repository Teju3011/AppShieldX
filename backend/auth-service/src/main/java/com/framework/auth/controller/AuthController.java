package com.framework.auth.controller;

import com.framework.auth.dto.*;
import com.framework.auth.service.AuthService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Controller exposing authentication endpoints for registration, login, token rotation, and logout.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<UserDto> register(
            @Valid @RequestBody RegisterRequest request,
            @RequestHeader(value = "X-Correlation-ID", required = false) String correlationId,
            HttpServletRequest httpRequest
    ) {
        String ipAddress = extractClientIp(httpRequest);
        UserDto user = authService.register(request, ipAddress, correlationId != null ? correlationId : "N/A");
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(
            @Valid @RequestBody LoginRequest request,
            @RequestHeader(value = "X-Correlation-ID", required = false) String correlationId,
            HttpServletRequest httpRequest
    ) {
        String ipAddress = extractClientIp(httpRequest);
        AuthResponse response = authService.login(request, ipAddress, correlationId != null ? correlationId : "N/A");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/refresh")
    public ResponseEntity<TokenRefreshResponse> refresh(
            @Valid @RequestBody TokenRefreshRequest request,
            @RequestHeader(value = "X-Correlation-ID", required = false) String correlationId,
            HttpServletRequest httpRequest
    ) {
        String ipAddress = extractClientIp(httpRequest);
        TokenRefreshResponse response = authService.refreshToken(request, ipAddress, correlationId != null ? correlationId : "N/A");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/logout")
    public ResponseEntity<MessageResponse> logout(
            @RequestHeader(value = "Authorization", required = false) String authHeader,
            @RequestHeader(value = "X-Correlation-ID", required = false) String correlationId,
            HttpServletRequest httpRequest
    ) {
        String ipAddress = extractClientIp(httpRequest);
        authService.logout(authHeader, ipAddress, correlationId != null ? correlationId : "N/A");
        return ResponseEntity.ok(new MessageResponse("Session terminated successfully"));
    }

    private String extractClientIp(HttpServletRequest request) {
        String xForwardedFor = request.getHeader("X-Forwarded-For");
        if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
            return xForwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }
}
