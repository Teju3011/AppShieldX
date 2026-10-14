package com.framework.threat;

import com.framework.threat.service.ThreatCacheService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
@DisplayName("ThreatDetectionService Application Context Test")
class ThreatDetectionServiceApplicationTests {

    @MockBean
    private ThreatCacheService threatCacheService;

    @Test
    @DisplayName("Application context should load successfully")
    void contextLoads() {
    }
}
