package com.framework.gateway.filter;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.data.redis.core.ReactiveStringRedisTemplate;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;
import reactor.core.publisher.Mono;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * Gateway filter validating JWT signatures, checking token revocation in Redis,
 * enforcing Role-Based Access Control (RBAC), and propagating authenticated identity downstream.
 */
@Component
public class JwtAuthenticationGatewayFilterFactory
        extends AbstractGatewayFilterFactory<JwtAuthenticationGatewayFilterFactory.Config> {

    private static final Logger log = LoggerFactory.getLogger(JwtAuthenticationGatewayFilterFactory.class);
    private final ReactiveStringRedisTemplate redisTemplate;
    private final SecretKey signingKey;

    public JwtAuthenticationGatewayFilterFactory(
            ReactiveStringRedisTemplate redisTemplate,
            @Value("${security.jwt.secret}") String jwtSecret
    ) {
        super(Config.class);
        this.redisTemplate = redisTemplate;
        this.signingKey = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
    }

    public static class Config {
        private boolean requireAdmin = false;

        public boolean isRequireAdmin() {
            return requireAdmin;
        }

        public void setRequireAdmin(boolean requireAdmin) {
            this.requireAdmin = requireAdmin;
        }
    }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            ServerHttpRequest request = exchange.getRequest();
            String path = request.getPath().value();

            // Allow anonymous access to authentication routes
            if (path.startsWith("/api/auth/") || path.startsWith("/api/v1/auth/")) {
                return chain.filter(exchange);
            }

            String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
            if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                log.warn("Unauthorized request to protected path {}: Missing or malformed Authorization header", path);
                return Mono.error(new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Missing or invalid Authorization header"));
            }

            String token = authHeader.substring(7).trim();

            // 1. Verify token is not blacklisted/revoked in Redis
            return redisTemplate.hasKey("token_blacklist:" + token)
                    .flatMap(isBlacklisted -> {
                        if (Boolean.TRUE.equals(isBlacklisted)) {
                            log.warn("Rejected blacklisted/revoked JWT on path: {}", path);
                            return Mono.error(new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Token has been revoked"));
                        }

                        // 2. Parse and cryptographically validate JWT claims
                        Claims claims;
                        try {
                            claims = Jwts.parser()
                                    .verifyWith(signingKey)
                                    .build()
                                    .parseSignedClaims(token)
                                    .getPayload();
                        } catch (JwtException e) {
                            log.warn("Invalid JWT cryptographic verification failed: {}", e.getMessage());
                            return Mono.error(new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid or expired JWT token"));
                        }

                        String userId = claims.getSubject();
                        @SuppressWarnings("unchecked")
                        List<String> roles = claims.get("roles", List.class);

                        // 3. Enforce RBAC for Admin routes
                        if (path.startsWith("/api/admin/") || path.startsWith("/api/v1/admin/") || config.isRequireAdmin()) {
                            if (roles == null || !roles.contains("ROLE_ADMIN")) {
                                log.warn("Access Denied: User {} lacks ROLE_ADMIN for path {}", userId, path);
                                return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN, "Insufficient privileges for administrative resource"));
                            }
                        }

                        // 4. Inject authenticated identity into mutated request headers for downstream microservices
                        ServerHttpRequest mutatedRequest = request.mutate()
                                .header("X-User-Id", userId != null ? userId : "")
                                .header("X-User-Roles", roles != null ? String.join(",", roles) : "")
                                .build();

                        return chain.filter(exchange.mutate().request(mutatedRequest).build());
                    });
        };
    }
}
