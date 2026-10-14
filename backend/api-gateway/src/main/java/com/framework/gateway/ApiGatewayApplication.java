package com.framework.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Cloud API Gateway Service Entry Point.
 *
 * Provides non-blocking reactive routing, edge JWT authentication,
 * Redis sliding-window rate limiting, and security header injection.
 */
@SpringBootApplication
public class ApiGatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}
