package com.framework.gateway.config;

import org.springframework.cloud.gateway.filter.ratelimit.KeyResolver;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import reactor.core.publisher.Mono;

import java.net.InetSocketAddress;

/**
 * KeyResolvers configuring client partition keys for distributed rate limiting.
 */
@Configuration
public class RedisRateLimiterConfig {

    @Bean
    @Primary
    public KeyResolver ipKeyResolver() {
        return exchange -> {
            String xForwardedFor = exchange.getRequest().getHeaders().getFirst("X-Forwarded-For");
            if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
                return Mono.just(xForwardedFor.split(",")[0].trim());
            }
            InetSocketAddress remoteAddress = exchange.getRequest().getRemoteAddress();
            if (remoteAddress != null && remoteAddress.getAddress() != null) {
                return Mono.just(remoteAddress.getAddress().getHostAddress());
            }
            return Mono.just("anonymous_ip");
        };
    }

    @Bean
    public KeyResolver deviceKeyResolver() {
        return exchange -> {
            String deviceId = exchange.getRequest().getHeaders().getFirst("X-Device-ID");
            return Mono.just(deviceId != null && !deviceId.isEmpty() ? deviceId : "unknown_device");
        };
    }

    @Bean
    public KeyResolver userKeyResolver() {
        return exchange -> {
            String userId = exchange.getRequest().getHeaders().getFirst("X-User-Id");
            return Mono.just(userId != null && !userId.isEmpty() ? userId : "anonymous_user");
        };
    }
}
