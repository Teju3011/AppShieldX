package com.framework.business.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;

public record CreateRecordRequest(
        @NotBlank(message = "Title is required")
        @Size(min = 2, max = 100, message = "Title must be between 2 and 100 characters")
        String title,

        @NotBlank(message = "Category is required")
        @Size(max = 50, message = "Category cannot exceed 50 characters")
        String category,

        @NotBlank(message = "Sensitive data payload is required")
        String sensitiveData,

        @DecimalMin(value = "0.00", message = "Amount must be zero or positive")
        BigDecimal amount
) {}
