package com.framework.auth.service.impl;

import com.framework.auth.dto.*;
import com.framework.auth.entity.RefreshToken;
import com.framework.auth.entity.Role;
import com.framework.auth.entity.User;
import com.framework.auth.repository.RefreshTokenRepository;
import com.framework.auth.repository.RoleRepository;
import com.framework.auth.repository.UserRepository;
import com.framework.auth.service.AuthService;
import com.framework.auth.service.JwtTokenProvider;
import com.framework.auth.service.TokenBlacklistService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.time.Duration;
import java.time.Instant;
import java.util.Collections;
import java.util.List;

/**
 * Implementation of AuthService managing secure authentication, token rotation, and credential hashing.
 */
@Service
public class AuthServiceImpl implements AuthService {

    private static final Logger log = LoggerFactory.getLogger(AuthServiceImpl.class);

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final RefreshTokenRepository refreshTokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final TokenBlacklistService tokenBlacklistService;

    @Value("${security.jwt.refresh-expiration-ms:604800000}")
    private long refreshExpirationMs;

    public AuthServiceImpl(
            UserRepository userRepository,
            RoleRepository roleRepository,
            RefreshTokenRepository refreshTokenRepository,
            PasswordEncoder passwordEncoder,
            JwtTokenProvider jwtTokenProvider,
            TokenBlacklistService tokenBlacklistService
    ) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.refreshTokenRepository = refreshTokenRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
        this.tokenBlacklistService = tokenBlacklistService;
    }

    @Override
    @Transactional
    public UserDto register(RegisterRequest request, String ipAddress, String correlationId) {
        log.info("Processing registration request for email: {} [CorrelationId: {}]", request.email(), correlationId);

        if (userRepository.existsByEmail(request.email().trim())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Email is already registered");
        }
        if (userRepository.existsByUsername(request.username().trim())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username is already taken");
        }

        Role userRole = roleRepository.findByName("ROLE_USER")
                .orElseGet(() -> roleRepository.save(new Role("ROLE_USER", "Standard application user")));

        String hashedPassword = passwordEncoder.encode(request.password());
        User user = new User(request.username().trim(), request.email().trim(), hashedPassword);
        user.getRoles().add(userRole);

        User savedUser = userRepository.save(user);

        log.info("User registered successfully [UserId: {}, CorrelationId: {}]", savedUser.getId(), correlationId);

        return new UserDto(
                savedUser.getId(),
                savedUser.getUsername(),
                savedUser.getEmail(),
                List.of("ROLE_USER")
        );
    }

    @Override
    @Transactional
    public AuthResponse login(LoginRequest request, String ipAddress, String correlationId) {
        log.info("Processing authentication attempt for email: {} [CorrelationId: {}]", request.email(), correlationId);

        User user = userRepository.findByEmail(request.email().trim())
                .orElseThrow(() -> {
                    recordFailedAuthAttempt(request.email(), ipAddress, correlationId);
                    return new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid email or password");
                });

        if (!user.isEnabled()) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "User account is disabled");
        }
        if (user.isAccountLocked()) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "User account is locked due to security policy");
        }

        if (!passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            recordFailedAuthAttempt(request.email(), ipAddress, correlationId);
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid email or password");
        }

        // Generate Access and Refresh Tokens
        String accessToken = jwtTokenProvider.generateAccessToken(user);
        String rawRefreshToken = jwtTokenProvider.generateRefreshTokenString();
        String hashedRefreshToken = jwtTokenProvider.hashToken(rawRefreshToken);

        Instant expiryDate = Instant.now().plusMillis(refreshExpirationMs);
        RefreshToken refreshToken = new RefreshToken(user, hashedRefreshToken, expiryDate);
        refreshTokenRepository.save(refreshToken);

        log.info("Authentication successful [UserId: {}, CorrelationId: {}]", user.getId(), correlationId);

        List<String> roles = user.getRoles().stream().map(Role::getName).toList();
        UserDto userDto = new UserDto(user.getId(), user.getUsername(), user.getEmail(), roles);

        return AuthResponse.of(
                accessToken,
                rawRefreshToken,
                jwtTokenProvider.getExpirationMs() / 1000,
                userDto
        );
    }

    @Override
    @Transactional
    public TokenRefreshResponse refreshToken(TokenRefreshRequest request, String ipAddress, String correlationId) {
        String hashedIncoming = jwtTokenProvider.hashToken(request.refreshToken());

        RefreshToken token = refreshTokenRepository.findByTokenHash(hashedIncoming)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid refresh token"));

        if (token.isRevoked() || token.getExpiryDate().isBefore(Instant.now())) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Refresh token is expired or revoked");
        }

        User user = token.getUser();

        // Token Rotation: Revoke previous token and commit new one
        token.setRevoked(true);
        refreshTokenRepository.save(token);

        String newAccessToken = jwtTokenProvider.generateAccessToken(user);
        String newRawRefreshToken = jwtTokenProvider.generateRefreshTokenString();
        String newHashedRefreshToken = jwtTokenProvider.hashToken(newRawRefreshToken);

        RefreshToken newToken = new RefreshToken(
                user,
                newHashedRefreshToken,
                Instant.now().plusMillis(refreshExpirationMs)
        );
        refreshTokenRepository.save(newToken);

        log.info("Token rotated successfully [UserId: {}, CorrelationId: {}]", user.getId(), correlationId);

        return TokenRefreshResponse.of(
                newAccessToken,
                newRawRefreshToken,
                jwtTokenProvider.getExpirationMs() / 1000
        );
    }

    @Override
    @Transactional
    public void logout(String authHeader, String ipAddress, String correlationId) {
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7).trim();
            tokenBlacklistService.blacklistToken(token, Duration.ofMinutes(15));
            log.info("Token committed to revocation list [CorrelationId: {}]", correlationId);
        }
    }

    private void recordFailedAuthAttempt(String email, String ipAddress, String correlationId) {
        log.warn("AUTH_FAILURE: Failed login attempt for email {} from IP {} [CorrelationId: {}]",
                email, ipAddress, correlationId);
        tokenBlacklistService.recordFailedAttempt(ipAddress);
    }
}
