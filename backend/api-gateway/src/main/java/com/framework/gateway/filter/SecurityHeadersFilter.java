package com.framework.gateway.filter;

import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/**
 * GlobalFilter injecting industry-standard security hardening headers on all responses.
 */
@Component
public class SecurityHeadersFilter implements GlobalFilter, Ordered {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        return chain.filter(exchange).then(Mono.fromRunnable(() -> {
            HttpHeaders headers = exchange.getResponse().getHeaders();

            // HTTP Strict Transport Security (HSTS)
            headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");

            // MIME Sniffing Protection
            headers.set("X-Content-Type-Options", "nosniff");

            // Clickjacking Defense
            headers.set("X-Frame-Options", "DENY");

            // Cross-Site Scripting Filter
            headers.set("X-XSS-Protection", "1; mode=block");

            // Content Security Policy
            headers.set("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'");

            // Referrer Policy
            headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

            // Cache Control for Sensitive API Responses
            if (!headers.containsKey("Cache-Control")) {
                headers.set("Cache-Control", "no-store, no-cache, must-revalidate");
            }
        }));
    }

    @Override
    public int getOrder() {
        return Ordered.LOWEST_PRECEDENCE; // Execute on outbound response path
    }
}
