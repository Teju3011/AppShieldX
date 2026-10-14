package com.framework.business.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.security.core.context.SecurityContextHolder;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("ZeroTrustSecurityFilter Unit Tests")
class ZeroTrustSecurityFilterTest {

    private JwtValidator jwtValidator;

    @Mock
    private FilterChain filterChain;

    private ZeroTrustSecurityFilter filter;
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        jwtValidator = new JwtValidator("404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970");
        objectMapper = new ObjectMapper().findAndRegisterModules();
        filter = new ZeroTrustSecurityFilter(jwtValidator, objectMapper, 69);
        SecurityContextHolder.clearContext();
    }

    @Test
    @DisplayName("Should block POST request when X-Device-Risk-Score exceeds threshold (Zero-Trust)")
    void testBlockHighRiskDeviceOnMutation() throws ServletException, IOException {
        MockHttpServletRequest request = new MockHttpServletRequest("POST", "/api/business/records");
        request.addHeader("X-Device-Risk-Score", "85"); // High risk score (e.g. Rooted / Frida active)
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilterInternal(request, response, filterChain);

        assertEquals(403, response.getStatus());
        assertTrue(response.getContentAsString().contains("Zero-Trust Enforcement"));
        verify(filterChain, never()).doFilter(any(), any());
    }

    @Test
    @DisplayName("Should permit request when X-Device-Risk-Score is within safe threshold")
    void testPermitLowRiskDevice() throws ServletException, IOException {
        MockHttpServletRequest request = new MockHttpServletRequest("POST", "/api/business/records");
        request.addHeader("X-Device-Risk-Score", "10"); // Low risk (Clean device)
        request.addHeader("X-User-Id", "42f9b8c2-2e0e-43a9-9e8c-5290b21a1e64");
        request.addHeader("X-User-Roles", "ROLE_USER");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilterInternal(request, response, filterChain);

        assertEquals(200, response.getStatus());
        verify(filterChain, times(1)).doFilter(request, response);
        assertNotNull(SecurityContextHolder.getContext().getAuthentication());
    }

    @Test
    @DisplayName("Should populate Correlation ID in response header if missing in request")
    void testInjectCorrelationId() throws ServletException, IOException {
        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/api/business/records");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilterInternal(request, response, filterChain);

        assertNotNull(response.getHeader("X-Correlation-ID"));
        verify(filterChain, times(1)).doFilter(request, response);
    }
}
