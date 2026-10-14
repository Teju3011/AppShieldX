package com.framework.auth.service;

import com.framework.auth.dto.*;
import com.framework.auth.entity.RefreshToken;
import com.framework.auth.entity.Role;
import com.framework.auth.entity.User;
import com.framework.auth.repository.RefreshTokenRepository;
import com.framework.auth.repository.RoleRepository;
import com.framework.auth.repository.UserRepository;
import com.framework.auth.service.impl.AuthServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.server.ResponseStatusException;

import java.time.Duration;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("AuthService Unit Tests")
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private RoleRepository roleRepository;

    @Mock
    private RefreshTokenRepository refreshTokenRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    private JwtTokenProvider jwtTokenProvider;

    @Mock
    private TokenBlacklistService tokenBlacklistService;

    private AuthServiceImpl authService;

    private User sampleUser;
    private Role userRole;

    @BeforeEach
    void setUp() {
        jwtTokenProvider = new JwtTokenProvider(
                "404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970",
                900000L,
                "test-issuer"
        );

        authService = new AuthServiceImpl(
                userRepository,
                roleRepository,
                refreshTokenRepository,
                passwordEncoder,
                jwtTokenProvider,
                tokenBlacklistService
        );

        userRole = new Role("ROLE_USER", "Standard user role");
        sampleUser = new User("alice", "alice@example.com", "encoded_secret");
        sampleUser.setId(UUID.randomUUID());
        sampleUser.getRoles().add(userRole);
    }

    @Test
    @DisplayName("Should successfully register a new user with default role")
    void testRegisterSuccess() {
        RegisterRequest request = new RegisterRequest("alice", "alice@example.com", "P@ssw0rd123!");

        when(userRepository.existsByEmail("alice@example.com")).thenReturn(false);
        when(userRepository.existsByUsername("alice")).thenReturn(false);
        when(roleRepository.findByName("ROLE_USER")).thenReturn(Optional.of(userRole));
        when(passwordEncoder.encode("P@ssw0rd123!")).thenReturn("encoded_secret");
        when(userRepository.save(any(User.class))).thenReturn(sampleUser);

        UserDto result = authService.register(request, "127.0.0.1", "test-corr-id");

        assertNotNull(result);
        assertEquals("alice", result.username());
        assertEquals("alice@example.com", result.email());
        assertTrue(result.roles().contains("ROLE_USER"));
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("Should reject registration if email already exists")
    void testRegisterConflictEmail() {
        RegisterRequest request = new RegisterRequest("alice", "alice@example.com", "P@ssw0rd123!");
        when(userRepository.existsByEmail("alice@example.com")).thenReturn(true);

        assertThrows(ResponseStatusException.class, () ->
                authService.register(request, "127.0.0.1", "test-corr-id")
        );
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("Should authenticate valid user and issue token pair")
    void testLoginSuccess() {
        LoginRequest request = new LoginRequest("alice@example.com", "P@ssw0rd123!");

        when(userRepository.findByEmail("alice@example.com")).thenReturn(Optional.of(sampleUser));
        when(passwordEncoder.matches("P@ssw0rd123!", "encoded_secret")).thenReturn(true);

        AuthResponse response = authService.login(request, "127.0.0.1", "test-corr-id");

        assertNotNull(response);
        assertNotNull(response.accessToken());
        assertNotNull(response.refreshToken());
        assertEquals("Bearer", response.tokenType());
        verify(refreshTokenRepository, times(1)).save(any(RefreshToken.class));
    }

    @Test
    @DisplayName("Should fail authentication on invalid password")
    void testLoginInvalidPassword() {
        LoginRequest request = new LoginRequest("alice@example.com", "WrongPassword!");

        when(userRepository.findByEmail("alice@example.com")).thenReturn(Optional.of(sampleUser));
        when(passwordEncoder.matches("WrongPassword!", "encoded_secret")).thenReturn(false);

        assertThrows(ResponseStatusException.class, () ->
                authService.login(request, "127.0.0.1", "test-corr-id")
        );
        verify(refreshTokenRepository, never()).save(any(RefreshToken.class));
        verify(tokenBlacklistService, times(1)).recordFailedAttempt("127.0.0.1");
    }

    @Test
    @DisplayName("Should rotate refresh token and issue new token pair")
    void testRefreshTokenSuccess() {
        String rawToken = "my-test-refresh-token-1234567890";
        String hashedToken = jwtTokenProvider.hashToken(rawToken);
        TokenRefreshRequest request = new TokenRefreshRequest(rawToken);
        RefreshToken storedToken = new RefreshToken(sampleUser, hashedToken, Instant.now().plusSeconds(3600));

        when(refreshTokenRepository.findByTokenHash(hashedToken)).thenReturn(Optional.of(storedToken));

        TokenRefreshResponse response = authService.refreshToken(request, "127.0.0.1", "test-corr-id");

        assertNotNull(response);
        assertNotNull(response.accessToken());
        assertNotNull(response.refreshToken());
        assertTrue(storedToken.isRevoked(), "Original refresh token must be revoked");
        verify(refreshTokenRepository, times(2)).save(any(RefreshToken.class));
    }

    @Test
    @DisplayName("Should revoke access token on logout into Redis blacklist")
    void testLogoutBlacklist() {
        authService.logout("Bearer valid.access.token", "127.0.0.1", "test-corr-id");

        verify(tokenBlacklistService, times(1)).blacklistToken(
                eq("valid.access.token"),
                eq(Duration.ofMinutes(15))
        );
    }
}
