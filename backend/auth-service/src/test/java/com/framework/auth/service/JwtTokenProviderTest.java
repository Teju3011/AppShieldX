package com.framework.auth.service;

import com.framework.auth.entity.Role;
import com.framework.auth.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("JwtTokenProvider Unit Tests")
class JwtTokenProviderTest {

    private JwtTokenProvider tokenProvider;
    private static final String SECRET = "404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970";
    private static final long EXPIRATION_MS = 900000L;
    private static final String ISSUER = "test-issuer";

    private User testUser;

    @BeforeEach
    void setUp() {
        tokenProvider = new JwtTokenProvider(SECRET, EXPIRATION_MS, ISSUER);

        testUser = new User("secops_user", "secops@enterprise.internal", "$2a$12$hashedPassword");
        testUser.setId(UUID.randomUUID());
        testUser.getRoles().add(new Role("ROLE_USER", "Standard User"));
        testUser.getRoles().add(new Role("ROLE_ADMIN", "Administrator"));
    }

    @Test
    @DisplayName("Should generate valid cryptographically signed JWT access token")
    void testGenerateAccessToken() {
        String token = tokenProvider.generateAccessToken(testUser);

        assertNotNull(token);
        assertTrue(token.split("\\.").length == 3, "JWT must contain header, payload, and signature");
        assertTrue(tokenProvider.validateToken(token));
        assertEquals(testUser.getId().toString(), tokenProvider.getUserIdFromToken(token));
    }

    @Test
    @DisplayName("Should reject tampered or malformed tokens")
    void testValidateTokenWithInvalidData() {
        assertFalse(tokenProvider.validateToken("invalid.token.structure"));
        assertFalse(tokenProvider.validateToken(""));
        assertFalse(tokenProvider.validateToken(null));

        String validToken = tokenProvider.generateAccessToken(testUser);
        String tamperedToken = validToken.substring(0, validToken.length() - 5) + "abcde";
        assertFalse(tokenProvider.validateToken(tamperedToken));
    }

    @Test
    @DisplayName("Should generate high-entropy opaque refresh tokens")
    void testGenerateRefreshTokenString() {
        String token1 = tokenProvider.generateRefreshTokenString();
        String token2 = tokenProvider.generateRefreshTokenString();

        assertNotNull(token1);
        assertNotNull(token2);
        assertNotEquals(token1, token2);
        assertEquals(64, token1.length());
    }

    @Test
    @DisplayName("Should compute deterministic SHA-256 token hash")
    void testHashToken() {
        String rawToken = "550e8400e29b41d4a716446655440000";
        String hash1 = tokenProvider.hashToken(rawToken);
        String hash2 = tokenProvider.hashToken(rawToken);

        assertNotNull(hash1);
        assertEquals(hash1, hash2);
        assertEquals(64, hash1.length()); // SHA-256 hex string is 64 chars
    }
}
