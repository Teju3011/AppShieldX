package com.framework.auth;

import com.framework.auth.service.TokenBlacklistService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
@DisplayName("AuthService Application Context Test")
class AuthServiceApplicationTests {

    @MockBean
    private TokenBlacklistService tokenBlacklistService;

    @Test
    @DisplayName("Application context should load successfully")
    void contextLoads() {
    }
}
