package com.healthcare.api.security;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Healthcare Application Backend Filter Reusing AppShieldX Risk Evaluation.
 * 
 * Reusability Metrics:
 * - Integration Steps: 2 (Add Maven dependency, Register Filter)
 * - Lines of Code: ~30 LOC
 * - Changes to AppShieldX Correlation Engine: 0
 */
public class HealthcareZeroTrustFilter implements Filter {

    private static final int RISK_THRESHOLD_RESTRICT = 75;

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // Step 1: Read authoritative risk score forwarded by AppShieldX Gateway
        String riskHeader = httpRequest.getHeader("X-Device-Risk-Score");
        String correlationId = httpRequest.getHeader("X-Correlation-ID");

        if (riskHeader != null) {
            try {
                int riskScore = Integer.parseInt(riskHeader.trim());
                String method = httpRequest.getMethod();

                // Step 2: Enforce Band 4 (RESTRICT_SENSITIVE_ACTIONS) on mutating medical records
                if (riskScore >= RISK_THRESHOLD_RESTRICT && ("POST".equalsIgnoreCase(method) || "PUT".equalsIgnoreCase(method) || "DELETE".equalsIgnoreCase(method))) {
                    httpResponse.setStatus(HttpServletResponse.SC_FORBIDDEN);
                    httpResponse.setContentType("application/json");
                    httpResponse.setHeader("X-Correlation-ID", correlationId);
                    httpResponse.getWriter().write("""
                        {"error": "Forbidden", "message": "AppShieldX Zero-Trust: Elevated device risk restricted medical record update", "correlationId": "%s"}
                    """.formatted(correlationId));
                    return;
                }
            } catch (NumberFormatException ignored) {}
        }

        chain.doFilter(request, response);
    }
}
