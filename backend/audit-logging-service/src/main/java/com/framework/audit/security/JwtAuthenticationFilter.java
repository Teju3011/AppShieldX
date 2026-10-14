package com.framework.audit.security;

import io.jsonwebtoken.Claims;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.MDC;
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
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtValidator jwtValidator;

    public JwtAuthenticationFilter(JwtValidator jwtValidator) {
        this.jwtValidator = jwtValidator;
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {

        String correlationId = request.getHeader("X-Correlation-ID");
        if (correlationId == null || correlationId.isBlank()) {
            correlationId = UUID.randomUUID().toString();
        }
        MDC.put("X-Correlation-ID", correlationId);
        response.setHeader("X-Correlation-ID", correlationId);

        try {
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
