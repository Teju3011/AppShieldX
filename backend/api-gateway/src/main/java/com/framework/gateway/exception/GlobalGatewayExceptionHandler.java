package com.framework.gateway.exception;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.framework.gateway.dto.StandardErrorResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.web.reactive.error.ErrorWebExceptionHandler;
import org.springframework.core.annotation.Order;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/**
 * Global reactive error handler translating exceptions into the standardized RFC 7807 payload.
 */
@Component
@Order(-2)
public class GlobalGatewayExceptionHandler implements ErrorWebExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalGatewayExceptionHandler.class);
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public Mono<Void> handle(ServerWebExchange exchange, Throwable ex) {
        HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR;
        String errorMessage = "Internal Gateway Error";

        if (ex instanceof ResponseStatusException rse) {
            status = HttpStatus.valueOf(rse.getStatusCode().value());
            errorMessage = rse.getReason() != null ? rse.getReason() : rse.getMessage();
        } else if (ex.getMessage() != null) {
            errorMessage = ex.getMessage();
        }

        String correlationId = exchange.getRequest().getHeaders().getFirst("X-Correlation-ID");
        String path = exchange.getRequest().getPath().value();

        log.error("Gateway error intercepted [Status: {}, Path: {}, CorrelationId: {}]: {}",
                status.value(), path, correlationId, ex.getMessage());

        StandardErrorResponse errorBody = StandardErrorResponse.of(
                status.value(),
                status.getReasonPhrase(),
                errorMessage,
                path,
                correlationId
        );

        exchange.getResponse().setStatusCode(status);
        exchange.getResponse().getHeaders().setContentType(MediaType.APPLICATION_JSON);
        if (correlationId != null) {
            exchange.getResponse().getHeaders().set("X-Correlation-ID", correlationId);
        }

        byte[] bytes;
        try {
            bytes = objectMapper.writeValueAsBytes(errorBody);
        } catch (JsonProcessingException e) {
            bytes = "{\"error\":\"Error serialization failed\"}".getBytes();
        }

        DataBuffer buffer = exchange.getResponse().bufferFactory().wrap(bytes);
        return exchange.getResponse().writeWith(Mono.just(buffer));
    }
}
