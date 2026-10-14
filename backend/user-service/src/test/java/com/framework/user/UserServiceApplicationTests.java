package com.framework.user;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
@DisplayName("UserService Application Context Test")
class UserServiceApplicationTests {

    @Test
    @DisplayName("Application context should load successfully")
    void contextLoads() {
    }
}
