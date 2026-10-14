package com.framework.business.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.framework.business.dto.StandardErrorResponse;
import io.jsonwebtoken.Claims;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

@Component
public class ZeroTrustSecurityFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(ZeroTrustSecurityFilter.class);

    private final JwtValidator jwtValidator;
    private final ObjectMapper objectMapper;
    private final int maxAllowedRiskScore;

    public ZeroTrustSecurityFilter(
            JwtValidator jwtValidator,
            ObjectMapper objectMapper,
            @Value("${security.zero-trust.max-allowed-risk-score:74}") int maxAllowedRiskScore
    ) {
        this.jwtValidator = jwtValidator;
        this.objectMapper = objectMapper;
        this.maxAllowedRiskScore = maxAllowedRiskScore;
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {

        // Track correlation ID
        String correlationId = request.getHeader("X-Correlation-ID");
        if (correlationId == null || correlationId.isBlank()) {
            correlationId = UUID.randomUUID().toString();
        }
        MDC.put("X-Correlation-ID", correlationId);
        response.setHeader("X-Correlation-ID", correlationId);

        try {
            // Check active experimental configuration bypass
            String expMode = request.getHeader("X-Experimental-Mode");
            boolean skipAdaptiveEnforcement = "CONFIG_A_API_ONLY".equalsIgnoreCase(expMode) ||
                    "CONFIG_B_MOBILE_ONLY".equalsIgnoreCase(expMode);

            // Zero-Trust RASP Context Verification: Check device risk score on state-modifying requests
            String riskHeader = request.getHeader("X-Device-Risk-Score");
            if (!skipAdaptiveEnforcement && riskHeader != null && !riskHeader.isBlank()) {
                try {
                    int riskScore = Integer.parseInt(riskHeader.trim());
                    String method = request.getMethod();
                    boolean isMutating = "POST".equalsIgnoreCase(method) || "PUT".equalsIgnoreCase(method) || "DELETE".equalsIgnoreCase(method);

                    // Response Band: RESTRICT_SENSITIVE_ACTIONS (75-100)
                    if (riskScore >= 75 && isMutating) {
                        log.warn("ZERO_TRUST_BLOCK: Request rejected due to elevated device risk score: {} [Path: {}, CorrelationId: {}]",
                                riskScore, request.getRequestURI(), correlationId);

                        response.setStatus(HttpStatus.FORBIDDEN.value());
                        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                        response.setHeader("X-Risk-Band", "RESTRICT_SENSITIVE_ACTIONS");

                        StandardErrorResponse error = StandardErrorResponse.of(
                                HttpStatus.FORBIDDEN.value(),
                                "Forbidden",
                                "Zero-Trust Enforcement: RESTRICT_SENSITIVE_ACTIONS (score " + riskScore + ") detected by cross-layer correlation. Transaction blocked.",
                                request.getRequestURI(),
                                correlationId
                        );

                        response.getWriter().write(objectMapper.writeValueAsString(error));
                        return;
                    }

                    // Response Band: STEP_UP_AUTHENTICATION (50-74)
                    if (riskScore >= 50 && riskScore < 75 && isMutating) {
                        String stepUpVerified = request.getHeader("X-Step-Up-Verified");
                        if (!"true".equalsIgnoreCase(stepUpVerified)) {
                            log.warn("ZERO_TRUST_STEP_UP: Step-up authentication required for risk score: {} [Path: {}, CorrelationId: {}]",
                                    riskScore, request.getRequestURI(), correlationId);

                            response.setStatus(HttpStatus.FORBIDDEN.value());
                            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                            response.setHeader("X-Risk-Band", "STEP_UP_AUTHENTICATION");
                            response.setHeader("X-Step-Up-Required", "true");

                            StandardErrorResponse error = StandardErrorResponse.of(
                                    HttpStatus.FORBIDDEN.value(),
                                    "Forbidden",
                                    "Zero-Trust Enforcement: STEP_UP_AUTHENTICATION required (risk score " + riskScore + "). Multi-factor step required.",
                                    request.getRequestURI(),
                                    correlationId
                                );

                            response.getWriter().write(objectMapper.writeValueAsString(error));
                            return;
                        }
                    }

                    // Response Band: MONITOR (25-49)
                    if (riskScore >= 25 && riskScore < 50) {
                        response.setHeader("X-Risk-Band", "MONITOR");
                        log.info("ZERO_TRUST_MONITOR: Monitored request from device with moderate risk: {} [Path: {}]",
                                riskScore, request.getRequestURI());
                    } else if (riskScore < 25) {
                        response.setHeader("X-Risk-Band", "ALLOW");
                    }
                } catch (NumberFormatException ignored) {
                    // Ignore malformed risk header, proceed to standard auth check
                }
            }

            // Identity verification from Gateway headers or JWT
            String gatewayUserId = request.getHeader("X-User-Id");
            String gatewayRoles = request.getHeader("X-User-Roles");

            if (gatewayUserId != null && !gatewayUserId.isBlank()) {
                List<SimpleGrantedAuthority> authorities = Collections.emptyList();
                if (gatewayRoles != null && !gatewayRoles.isBlank()) {
                    authorities = Arrays.stream(gatewayRoles.split(","))
                            .map(String::trim)
                            .map(r -> r.startsWith("ROLE_") ? r : "ROLE_" + r)
                            .map(SimpleGrantedAuthority::new)
                            .toList();
                }

                UsernamePasswordAuthenticationToken auth =
                        new UsernamePasswordAuthenticationToken(gatewayUserId, null, authorities);
                SecurityContextHolder.getContext().setAuthentication(auth);
            } else {
                String authHeader = request.getHeader("Authorization");
                if (authHeader != null && authHeader.startsWith("Bearer ")) {
                    String token = authHeader.substring(7).trim();
                    if (jwtValidator.validateToken(token)) {
                        Claims claims = jwtValidator.getClaims(token);
                        String userId = claims.getSubject();
                        List<String> roles = jwtValidator.extractRoles(claims);

                        List<SimpleGrantedAuthority> authorities = roles.stream()
                                .map(r -> r.startsWith("ROLE_") ? r : "ROLE_" + r)
                                .map(SimpleGrantedAuthority::new)
                                .toList();

                        UsernamePasswordAuthenticationToken auth =
                                new UsernamePasswordAuthenticationToken(userId, null, authorities);
                        SecurityContextHolder.getContext().setAuthentication(auth);
                    }
                }
            }

            filterChain.doFilter(request, response);
        } finally {
            MDC.remove("X-Correlation-ID");
        }
    }
}
