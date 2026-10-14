package com.framework.audit;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
@DisplayName("AuditLoggingService Application Context Test")
class AuditLoggingServiceApplicationTests {

    @Test
    @DisplayName("Application context should load successfully")
    void contextLoads() {
    }
}
