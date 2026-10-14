package com.framework.gateway.filter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.Ordered;
import org.springframework.data.redis.core.ReactiveStringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;

import java.net.InetSocketAddress;
import java.time.Duration;
import java.time.Instant;

/**
 * Reactive Redis-backed sliding-window rate limiter.
 *
 * Enforces differentiated rate limiting thresholds for login (5/min),
 * general API (100/min), and security telemetry ingestion (20/min).
 */
@Component
public class RateLimitEnforcementFilter implements WebFilter, Ordered {

    private static final Logger log = LoggerFactory.getLogger(RateLimitEnforcementFilter.class);
    private final ReactiveStringRedisTemplate redisTemplate;

    @Value("${security.rate-limit.login-per-minute:5}")
    private long loginLimit;

    @Value("${security.rate-limit.api-per-minute:100}")
    private long generalApiLimit;

    @Value("${security.rate-limit.security-events-per-minute:20}")
    private long securityEventsLimit;

    public RateLimitEnforcementFilter(ReactiveStringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String path = exchange.getRequest().getPath().value();

        // Skip rate-limiting for actuator metrics/health scraping
        if (path.startsWith("/actuator/")) {
            return chain.filter(exchange);
        }

        String clientIp = extractClientIp(exchange);
        String deviceId = exchange.getRequest().getHeaders().getFirst("X-Device-ID");

        long limit;
        String partitionKey;

        if (path.contains("/api/auth/login")) {
            limit = loginLimit;
            partitionKey = "rate_limit:login:" + clientIp;
        } else if (path.contains("/api/security/events")) {
            limit = securityEventsLimit;
            partitionKey = "rate_limit:events:" + (deviceId != null ? deviceId : clientIp);
        } else {
            limit = generalApiLimit;
            partitionKey = "rate_limit:general:" + clientIp;
        }

        long currentMinute = Instant.now().getEpochSecond() / 60;
        String redisKey = partitionKey + ":" + currentMinute;

        return redisTemplate.opsForValue().increment(redisKey)
                .flatMap(count -> {
                    if (count == 1) {
                        // Set 65-second expiration to cover window boundary
                        return redisTemplate.expire(redisKey, Duration.ofSeconds(65))
                                .thenReturn(count);
                    }
                    return Mono.just(count);
                })
                .flatMap(count -> {
                    if (count > limit) {
                        log.warn("RATE_LIMIT_EXCEEDED: Key {} exceeded limit of {} (Current count: {}) on path {}",
                                redisKey, limit, count, path);

                        exchange.getResponse().getHeaders().set("Retry-After", "60");
                        exchange.getResponse().getHeaders().set("X-RateLimit-Limit", String.valueOf(limit));
                        exchange.getResponse().getHeaders().set("X-RateLimit-Remaining", "0");

                        return Mono.error(new ResponseStatusException(
                                HttpStatus.TOO_MANY_REQUESTS,
                                "Rate limit exceeded. Maximum " + limit + " requests allowed per minute."
                        ));
                    }

                    long remaining = Math.max(0, limit - count);
                    exchange.getResponse().getHeaders().set("X-RateLimit-Limit", String.valueOf(limit));
                    exchange.getResponse().getHeaders().set("X-RateLimit-Remaining", String.valueOf(remaining));

                    return chain.filter(exchange);
                });
    }

    private String extractClientIp(ServerWebExchange exchange) {
        String xForwardedFor = exchange.getRequest().getHeaders().getFirst("X-Forwarded-For");
        if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
            return xForwardedFor.split(",")[0].trim();
        }
        InetSocketAddress remoteAddress = exchange.getRequest().getRemoteAddress();
        if (remoteAddress != null && remoteAddress.getAddress() != null) {
            return remoteAddress.getAddress().getHostAddress();
        }
        return "127.0.0.1";
    }

    @Override
    public int getOrder() {
        return -50; // Execute right after correlation ID generation
    }
}
